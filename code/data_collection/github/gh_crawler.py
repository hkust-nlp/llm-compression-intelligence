import requests
import sys
import time
import json
import os
import argparse
# Insert GitHub API token here, in place of *TOKEN*.
headers = {"Authorization": "token *TOKEN*"}


def run_query(max_stars):
	end_cursor = None  
	repositories = set()
	info_list={}
	while end_cursor != "":
		query = f"""
		{{
		  search(query: "language:{args.language} fork:false created:>{args.created_at} sort:stars stars:<{max_stars}", type: REPOSITORY, first: 100 {', after: "' + end_cursor + '"' if end_cursor else ''}) {{
			edges {{
			  node {{
				... on Repository {{
				  url
				  isPrivate
				  isDisabled
				  isLocked
				  createdAt
          		  pushedAt
          		  name
				  licenseInfo {{
					name
				  }}
				  owner {{
          			login
          		  }}
				  stargazers {{
					totalCount
				  }}
				}}
			  }}
			}}
			pageInfo {{
			  hasNextPage
			  endCursor
			}}
		  }}
		}}
		"""
		print(f'  Retrieving next page; {len(repositories)} repositories in this batch so far.')
		# Attempt a query up to three times, pausing when a query limit is hit.
		attempts = 0
		success = False
		while not success and attempts < 10:
			try:
				request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
				print(query)
				print(request)
				content = request.json()
				if 'data' not in content or 'search' not in content['data']:
					# If this is simply a signal to pause querying, wait two minutes.
					if 'message' in content and 'wait' in content['message']:
						attempts += 1
						time.sleep(120)
					# Otherwise, assume we've hit the end of the stream.
					else:
						break
				else:
					success = True
			except:
				continue
		if not success:
			break
		end_cursor = get_end_cursor(content)
		new_repositories, is_done,info = get_repositories(content)
		repositories.update(new_repositories)
		info_list.update(info)
		if len(repositories) > args.num_repos or is_done:
			break
	return repositories,info_list


def get_end_cursor(content):
	page_info = content['data']['search']['pageInfo']
	has_next_page = page_info['hasNextPage']
	if has_next_page:
		return page_info['endCursor']
	return ""


def get_repositories(content):
	edges = content['data']['search']['edges']
	repositories_with_stars = []
	info_list={}
	for edge in edges:
		if edge['node']['isPrivate'] is False and edge['node']['isDisabled'] is False and edge['node']['isLocked'] is False:
			repository = edge['node']['url']
			star_count = edge['node']['stargazers']['totalCount']
			info={
				"url":edge['node']['url'],
				"createdAt":edge['node']['createdAt'],
				'pushedAt':edge['node']['pushedAt'],
				"repo_name":f"{edge['node']['owner']['login']}/{edge['node']['name']}",
				"licenses":edge['node']['licenseInfo']["name"] if edge['node']['licenseInfo'] else "null",
				"stars_count":star_count
			}
			info_list[f"{edge['node']['owner']['login']}/{edge['node']['name']}"]=info
			if star_count < args.min_stars:
				return repositories_with_stars, True, info_list
			repositories_with_stars.append((repository, star_count))
			#info_list[f"{edge['node']['owner']['login']}/{edge['node']['name']}"]=info
	return repositories_with_stars, False,info_list


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--language", type=str, help="Language to search for.",default="python")
	parser.add_argument("--num_repos", type=int, help="Number of repositories to search for.",default=100)
	parser.add_argument("--min_stars", type=int, help="Minimum number of stars for a repository to be included.",default=10)
	parser.add_argument("--created_at", type=str, help="Date after which a repository is considered active.",default='2023-09-01')
	args = parser.parse_args()
	repositories = set()  # Keep track of a set of repositories seen to avoid duplicate entries across pages.
	next_max_stars = 1_000_000_000  # Initialize to a very high value.
	info_list={}
	if not os.path.exists(r"TopLists"):
		os.mkdir(r"TopLists")
	if not os.path.exists(r"InfoLists"):
		os.mkdir(r"InfoLists")
	retry=0
	with open(f'TopLists/{args.language}_top_repos.txt', 'w',encoding='utf-8') as f:
		while len(repositories) < args.num_repos:
			results,info = run_query(next_max_stars) # Get the next set of pages.
			info_list.update(info)
			if not results:
				break
			new_repositories = [repository for repository, _ in results]
			next_max_stars = min([stars for _, stars in results])
			
			# If a query returns no new repositories, drop it.
			if len(repositories | set(new_repositories)) == len(repositories):
				retry+=1
				if retry>5:
					break
			for repository, stars in sorted(results, key=lambda e: e[1], reverse=True):
				if repository not in repositories:
					repositories.add(repository)
					f.write(f'{stars}\t{repository}\n')
			f.flush()

			print(f'Collected {len(repositories):,} repositories so far; lowest number of stars: {next_max_stars:,}')
	with open(f'InfoLists/{args.language}_top_repos.json', 'w',encoding='utf-8') as f:
		json.dump(info_list,f,indent=4)
