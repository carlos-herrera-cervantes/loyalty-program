env=".env.test"

if [ -e "$1" ]
then
    env=$1
fi

export $(cat $env | grep -v ^# | xargs)

python3 -m unittest -v
