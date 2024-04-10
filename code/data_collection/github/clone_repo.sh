
in=$1
language=$2


repo=$(echo $in | cut -d$'\t' -f2);
name_part=$(echo $repo | cut -d"/" -f4-6);
name=$(echo $name_part | cut -d"/" -f2);
org=$(echo $name_part | cut -d"/" -f1);
echo "Cloning $org/$name"
DIR=Repos/$language/$org; \
OUT=Code/$language/$org; \

if [ -d $OUT/$name ]; then echo "deja vu"; exit; fi;
mkdir -p $DIR; \
mkdir -p $OUT; \


if [ ! -d $DIR/$name ]; then
  git clone -q --depth 1 https://github.com/$org/$name $DIR/$name;
fi;


python3 extract_code.py $language $DIR/$name $OUT/$name;
rm -rf $DIR/$name