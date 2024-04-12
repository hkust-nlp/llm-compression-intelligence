# ArXiv Collection Pipeline

This section describes the ArXiv paper collection pipeline, which mainly includes: downloading the ArXiv dump from Amazon Web Services (AWS), converting Latex source code to markdown using `pandoc`, and finally annotating the data and extracting papers with tags that contain math. The implementation of converting Latex source code to markdown refers to [The Pile](https://gist.github.com/leogao2/e09b64eae3b987925ccf3b86401624c6).

## Installation

* Install pandoc：

  ```cmd
  apt-get install pandoc
  ```

* Install Python packages:

  ```
  tqdm
  python-magic
  chardet
  s3cmd
  easydict
  ```



## Usage

**NOTE: Obtaining ArXiv data using the following steps may incur costs!**

- First, download the latest [ArXiv metadata](https://www.kaggle.com/datasets/Cornell-University/arxiv) from Kaggle, unzip it, and save it in the current directory named "arxiv-metadata-oai-snapshot.json".

- The Latex source files of ArXiv can be accessed through [AWS S3 Bulk Source File Access](https://info.arxiv.org/help/bulk_data_s3.html). To use AWS S3, you need to have an AWS account and apply for AWS security credentials. [How to apply?](https://aws.amazon.com/cn/blogs/security/how-to-find-update-access-keys-password-mfa-aws-management-console/)

- Configure S3 using the `s3cmd --configure` command and enter the obtained AWS security credentials.

- Download the ArXiv dump information from AWS S3:

  ```cmd
  s3cmd get s3://arxiv/src/arXiv_src_manifest.xml --requester-pays
  ```

- Configure the version of ArXiv dump and the number of segments to download in `run.sh`, then run the script. The processed data will be saved in the `math_data` folder.

  ```cmd
  bash run.sh 
  ```

  