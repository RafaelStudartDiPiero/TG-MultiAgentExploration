# Algorithm related to bachelor's thesis

## Executing Code

For running the code, you should must to make sure your python has the tkinter module.
After that, you can test the result by running the following command:

```python3 demo.py```

You can pass specific arguments to define parameters, like:

```--algorithm``` : Defines which algorithm should be used. Can be "self" or "tarry". The default value is self.

```--agents``` : Defines the number of agents that will be in the maze. The default value is 3.

```--maze``` : Defines the file of a maze that can be used to generate the maze. The default value is None.

As an example, you could run:

```python3 demo.py --agents 3 --graph test1.csv ```

And you have a demo using the Tarry Generalization Algoritm, five agents and in the maze salved in the test1.csv.

## Multi-agent graph exploration without communication

A in-depth analysis of the algoritm can be found here:

