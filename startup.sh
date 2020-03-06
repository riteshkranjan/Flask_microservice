source env/Scripts/activate

python sqrt/app.py 5000 &
echo $! >> pid.txt

python sqrt/app.py 5001 &
echo $! >> pid.txt

python prime/app.py 5002 &
echo $! >> pid.txt

python prime/app.py 5003 &
echo $! >> pid.txt

deactivate

cat pid.txt