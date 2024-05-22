# Algorithm related to bachelor's thesis

## Executing Code

For running the code, you should must to make sure your python has the tkinter module.
After that, you can test the result by running the following command:

```python3 demo.py```

You can pass specific arguments to define parameters, like:

```--algorithm``` : Defines which algorithm should be used. Can be "self" or "tarry". The default value is self.

```--agents``` : Defines the number of agents that will be in the graph. The default value is 3.

```--graph``` : Defines the file of a graph that can be used to generate the graph. The default value is None.

As an example, you could run:

```python3 demo.py --agents 3 --graph test1.csv```

```python3 demo.py --agents 3 --graph full_tree_test.graphml```

```python3 demo.py --agents 3 --graph test2.csv```

```python3 demo.py --agents 3 --graph testimperfect.csv```

```python3 demo.py --agents 3 --graph testperfect.csv```

```python3 demo.py --agents 3 --graph test1.csv --algorithm two_interval```

## Multi-agent graph exploration without communication

A in-depth analysis of the algoritm can be found here:

