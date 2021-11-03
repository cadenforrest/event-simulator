## How to Compile and Run this program

- Ensure that python3 is installed on your system. 
- After downloading the program, create a virtual environment

```
python3 -m venv my_environment
```

- Activate the virtual environment

```
source my_environment/bin/activate
```

- Install the requirements

```
pip install -r requirements.txt
pip3 install -r requirements.txt #<- if the above fails, use pip3 
```

To run a single instance of the program with a given lambda, do

```
python3 PA2.py --average-arrival-rate {your_value}
```

To run all instances of the program with lambdas 10-30 and generate plots, run 
```
python3 PA2.py --plot
```
