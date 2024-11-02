# Algorithm related to bachelor's thesis

## Executing Code

For running the code, you should must to make sure your python has the tkinter module.
After that, you can test the result by running the following command:

`python3 demo.py`

You can pass specific arguments to define parameters, like:

`--algorithm` : Defines which algorithm should be used. Can be "self" or "tarry". The default value is self.

`--agents` : Defines the number of agents that will be in the graph. The default value is 3.

`--graph` : Defines the file of a graph that can be used to generate the graph. The default value is None.

As an example, you could run:

`python3 demo.py --agents 3 --graph test1.csv`

`python3 demo.py --agents 3 --graph full_tree_test.graphml`

`python3 demo.py --agents 3 --graph test2.csv`

`python3 demo.py --agents 3 --graph testimperfect.csv`

`python3 demo.py --agents 3 --graph testperfect.csv`

`python3 demo.py --agents 3 --graph test1.csv --algorithm two_interval`

`python3 demo.py --agents 3 --graph test1.csv --algorithm tarry`

`python3 demo.py --agents 3 --graph test1.csv --algorithm tarry_interval_priority`

`python3 demo.py --agents 3 --graph test1.csv --algorithm tarry_interval_tie_breaker`

`python3 demo.py --agents 3 --graph test1.csv --algorithm tarry_delayed_interval_tie_breaker`

`python3 demo.py --agents 3 --graph "mazes/10_by_10/maze_10x10__1.csv"`

`python3 demo.py --agents 3 --graph "mazes/20_by_20/maze_20x20__1.csv"`

`python3 demo.py --agents 3 --graph "mazes/30_by_30/maze_30x30__1.csv"`

`python3 demo.py --agents 3 --graph "mazes/40_by_40/maze_40x40__1.csv"`

`python3 demo.py --agents 3 --graph "graphs/random_unlabeled_tree/100/graph_100__1.graphml" --algorithm tarry_delayed_interval_tie_breaker`

`python3 demo.py --agents 3 --graph "graphs/random_unlabeled_tree/250/graph_250__1.graphml" --algorithm tarry_delayed_interval_tie_breaker`

`python3 demo.py --agents 3 --graph "graphs/random_unlabeled_tree/500/graph_500__1.graphml" --algorithm tarry_delayed_interval_tie_breaker`

`python3 demo.py --agents 3 --graph "graphs/random_unlabeled_tree/1000/graph_1000__1.graphml" --algorithm tarry_delayed_interval_tie_breaker`


`python3 demo.py --agents 3 --graph graphs/barabasi_albert/100/graph_100__190.graphml --algorithm tarry_interval_priority`

## Generating Results

After making sure the simulation works, you can automatically generate results for multiple sets of graphs. This can take a long time.

You can pass specific arguments to define parameters, like:

`--algorithm` : Defines which algorithm should be used. Can be "self", "two_interval" or "tarry". The default value is self.

`--base_path` : Defines the path to the directory where all graphs as stored.

`--graph_size_path` : Defines specific size directory to use (e.g., '10_by_10', '20_by_20'). If not provided, all sizes found will be used.

`--max_agents` : Defines the maximum number of users to be simulated.

`--plot`: Defines if the plot should be generated.

As an example, you could run:

`python3 results.py --base_path mazes  --algorithm self --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm two_interval --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry --max_agents 40 --plot true`

`python3 results.py --base_path mazes --max_agents 40`

`python3 results.py --base_path mazes --algorithm tarry_interval_priority --graph_size_path 10_by_10 --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry_interval_priority --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry_interval_tie_breaker --graph_size_path 10_by_10 --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry_interval_tie_breaker --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 10_by_10 --max_agents 40 --plot true`

`python3 results.py --base_path mazes --algorithm tarry_delayed_interval_tie_breaker --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --graph_size_path 100 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --graph_size_path 250 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --graph_size_path 500 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --graph_size_path 1000 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/random_unlabeled_tree --graph_size_path 1500 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/barabasi_albert --algorithm self --graph_size_path 100 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm two --graph_size_path 100 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry --graph_size_path 100 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_priority --graph_size_path 100 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_tie_breaker --graph_size_path 100 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 100 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/barabasi_albert --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm self --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm two_interval --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_priority --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_tie_breaker --graph_size_path 250 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 250 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/barabasi_albert --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm self --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm two_interval --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_priority --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_tie_breaker --graph_size_path 500 --max_agents 40 --plot true`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 500 --max_agents 40 --plot true`

`python3 results.py --base_path graphs/barabasi_albert --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm self --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm two_interval --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_priority --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_interval_tie_breaker --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/barabasi_albert --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 1000 --max_agents 30 --plot false`

`python3 results.py --base_path graphs/small_world --graph_size_path 100  --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry --graph_size_path 100 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_priority --graph_size_path 100 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_tie_breaker --graph_size_path 100 --max_agents 40 --plot `

`python3 results.py --base_path graphs/small_world --graph_size_path 250  --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm self --graph_size_path 250 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm two_interval --graph_size_path 250 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry --graph_size_path 250 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_priority --graph_size_path 250 --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_tie_breaker --graph_size_path 250 --max_agents 40 --plot `
`python3 results.py --base_path graphs/small_world --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 250 --max_agents 40 --plot false `

`python3 results.py --base_path graphs/small_world --graph_size_path 500  --max_agents 40 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm self --graph_size_path 500 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm two_interval --graph_size_path 500 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry --graph_size_path 500 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_priority --graph_size_path 500 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_tie_breaker --graph_size_path 500 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 500 --max_agents 30 --plot false `

`python3 results.py --base_path graphs/small_world --algorithm self --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm two_interval --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_priority --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_interval_tie_breaker --graph_size_path 1000 --max_agents 30 --plot false`
`python3 results.py --base_path graphs/small_world --algorithm tarry_delayed_interval_tie_breaker --graph_size_path 1000 --max_agents 30 --plot false`

## Comparing Results

After generating results, you can generate specific plots to compare different algorithms.

You can pass specific arguments to define which and how they should be compared, like:

`--algorithms` : Defines which algorithm should be compared.

`--graph_size_path` : Defines specific size directory to use (e.g., '10_by_10', '20_by_20'). If not provided, all sizes found will be used.

`--metrics` : DefineS which metric should be used. Defaults to ALL.

`--split_legend` : Defines if the legend should be generated alongside the plot or separate.

`--title` : Defines if the title for the plot.

As an example, you could run:

`python3 compare.py --algorithms "self, two_interval, tarry" --base_path mazes --graph_size 40_by_40 --metrics "avg_pioneer_steps" --split_legend False --title "Algorithms Pioneer Steps - Comparison" `
`python3 compare.py --algorithms "self, two_interval, tarry" --base_path mazes --graph_size 40_by_40 --metrics "avg_fraction_pioneer" --split_legend False --title "Algorithms Pioneer Fraction - Comparison" `

`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker" --base_path mazes --graph_size 40_by_40 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants - Comparison" `
`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path mazes --graph_size 40_by_40 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants - Comparison" `

`python3 compare.py --algorithms "self, two_interval, tarry" --base_path graphs/random_unlabeled_tree --graph_size 100 --metrics "avg_pioneer_steps" --split_legend False --title "Algorithms Pioneer Steps Random Unlabeled - Comparison" `
`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/random_unlabeled_tree --graph_size 100 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants Random Unlabeled - Comparison" `

`python3 compare.py --algorithms "self, two_interval, tarry" --base_path graphs/barabasi_albert --graph_size 100 --metrics "avg_pioneer_steps" --split_legend True --title "Algorithms Pioneer Steps - Comparison - 100 Barabási-Albert Graph" `
`python3 compare.py --algorithms "self, two_interval, tarry" --base_path graphs/barabasi_albert --graph_size 100 --metrics "avg_fraction_pioneer" --split_legend True --title "Algorithms Pioneer Fraction - Comparison - 100 Barabási-Albert Graph" `

`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/barabasi_albert --graph_size 1000 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants Pioneer Steps- Comparison - 1000 Barabási-Albert Graph" `
`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/barabasi_albert --graph_size 1000 --metrics "avg_fraction_pioneer" --split_legend True --title "Tarry Variants Pioneer Fraction- Comparison - 1000 Barabási-Albert Graph" `

`python3 compare.py --algorithms "self, two_interval, tarry" --base_path graphs/small_world --graph_size 100 --metrics "avg_pioneer_steps" --split_legend True --title "Algorithms Pioneer Steps - Comparison - 100 Small World Graph" `
`python3 compare.py --algorithms "self, two_interval, tarry" --base_path graphs/small_world --graph_size 100 --metrics "avg_fraction_pioneer" --split_legend True --title "Algorithms Pioneer Fraction - Comparison - 100 Small World Graph" `

`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/small_world --graph_size 100 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants Pioneer Steps- Comparison - 100 Small World Graph" `
`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/small_world --graph_size 100 --metrics "avg_fraction_pioneer" --split_legend True --title "Tarry Variants Pioneer Fraction- Comparison - 100 Small World Graph" `
`python3 compare.py --algorithms "tarry,tarry_interval_priority,tarry_interval_tie_breaker, tarry_delayed_interval_tie_breaker" --base_path graphs/small_world --graph_size 100 --metrics "avg_pioneer_steps" --split_legend True --title "Tarry Variants Pioneer Steps- Comparison - 100 Small World Graph" --relative True `


## Graph Statistics

For a deeper analysis, we can calculate statistics related to the graphs used.

`--graph-path` : Defines which file path to saved graph(file) or saved graphs(directory) should be analysed.

As an example, you could run:

`python3 graph_statistics.py --graph-path "test1.csv" `
`python3 graph_statistics.py --graph-path "mazes/10_by_10" `
`python3 graph_statistics.py --graph-path "mazes/10_by_10/maze_10x10__1.csv" `
`python3 graph_statistics.py --graph-path "mazes/20_by_20" `
`python3 graph_statistics.py --graph-path "mazes/20_by_20/maze_20x20__1.csv" `
`python3 graph_statistics.py --graph-path "mazes/30_by_30" `
`python3 graph_statistics.py --graph-path "mazes/30_by_30/maze_30x30__1.csv" `
`python3 graph_statistics.py --graph-path "mazes/40_by_40" `
`python3 graph_statistics.py --graph-path "mazes/40_by_40/maze_40x40__1.csv" `

`python3 graph_statistics.py --graph-path "graphs/random_unlabeled_tree/100" `
`python3 graph_statistics.py --graph-path "graphs/barabasi_albert/100" `
`python3 graph_statistics.py --graph-path "graphs/small_world/100" `


## Generate Graphs

You can also create your own dataset of graphs.

`--graph_type` : Defines which generator should be used for creating the graphs.
`--graph_size` : Defines the size of the graph(number of nodes).
`--n_graph` : Defines how many graphs should be generated.

As an example, you could run:

`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 10 --n_graph 1 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 10 --n_graph 1 `

`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 100 --n_graph 250 `
`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 250 --n_graph 250 `
`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 500 --n_graph 250 `
`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 1000 --n_graph 250 `
`python3 generate_graphs.py --graph_type random_unlabeled_tree --graph_size 1500 --n_graph 250 `

`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 100 --n_graph 1 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 100 --n_graph 250 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 250 --n_graph 250 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 500 --n_graph 250 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 1000 --n_graph 250 `
`python3 generate_graphs.py --graph_type barabasi_albert --graph_size 1500 --n_graph 250 `

`python3 generate_graphs.py --graph_type small_world --graph_size 100 --n_graph 250 `
`python3 generate_graphs.py --graph_type small_world --graph_size 250 --n_graph 250 `
`python3 generate_graphs.py --graph_type small_world --graph_size 500 --n_graph 250 `
`python3 generate_graphs.py --graph_type small_world --graph_size 1000 --n_graph 250 `
`python3 generate_graphs.py --graph_type small_world --graph_size 1500 --n_graph 250 `

## Multi-agent graph exploration without communication

A in-depth analysis of the algoritm can be found here:
