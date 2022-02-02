from time import sleep
import graphviz
import dash_interactive_graphviz
import dash
import networkx as nx
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import node_manager
from threading import Thread

app = dash.Dash(__name__)

dot = nx.MultiDiGraph(directed=True)

app.layout = html.Div(
    [
        html.Div(
            dash_interactive_graphviz.DashInteractiveGraphviz(id="gv", dot_source=str(nx.drawing.nx_pydot.to_pydot(dot))),
            style=dict(flexGrow=1, position="relative"),
        ),
        html.Div(
            [
                html.H3("selected node id"),
                html.Div(id="node_id"),
                html.H3("enter data to add"),
                dcc.Textarea(
                    id="data_to_add",
                    style=dict(height=20, position="relative")
                ),
                html.Button("add_data", id="add_data_btn"),
                html.H3("selected node database"),
                dcc.Textarea(
                    id="database",
                    style=dict(flexGrow=0.5, position="relative")
                ),
                html.Button("remove_node", id="remove_btn", n_clicks=0, style={"margin-bottom": "15px"}),
                html.H3("node to add:", style={"margin-bottom": "1px"}),
                html.H3("enter node neighbors ex. (1, 2, 3)"),
                dcc.Textarea(
                    id="node_neighbors",
                    style=dict(height=20, position="relative")
                ),
                html.Button("add_node", id="add_btn", n_clicks=0, style={"margin-bottom": "15px"}),
            ],
            style=dict(display="flex", flexDirection="column"),
        ),
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)


@app.callback(Output("gv", "dot_source"),
              Input("add_btn", "n_clicks"), Input("remove_btn", "n_clicks"),
              State("node_neighbors", "value"), State("node_id", "children"))
def manage_nodes(_, __, node_neighbors, node_id):
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_id == "remove_btn":
        if node_id:
            node_manager.remove_node(int(node_id["props"]["children"]), dot)
    elif button_id == "add_btn":
        if node_neighbors:
            node_manager.add_node(list(map(int, node_neighbors.split(","))), dot)
        else:
            node_manager.add_node([], dot)
    return str(nx.drawing.nx_pydot.to_pydot(dot))


@app.callback(Output("node_id", "children"), Output("database", "value"),
              Input("gv", "selected_node"), Input("add_data_btn", "n_clicks"),
              State("data_to_add", "value"))
def manage_node(selected_node, _, data):
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if selected_node is None:
        selected_node = 0
    if button_id == "add_data_btn":
        node_manager.nodes[int(selected_node)].add_to_database(data)
    return html.Div(selected_node), str(node_manager.nodes[int(selected_node)].database.data)


if __name__ == "__main__":
    app.run_server(debug=True)

    # node_manager.add_node([])
    # node_manager.add_node([0])
    # node_manager.add_node([0, 1])
    # # node_manager.add_node([0, 1, 2])
    # node_manager.add_node([0])
    # # node_manager.add_node([4])
    # node_manager.nodes[0].add_to_database("hello")
    # node_manager.nodes[1].add_to_database("hello")
    # node_manager.nodes[1].add_to_database("yello")
    # # node_manager.nodes[2].add_to_database("hello")
    # node_manager.nodes[0].add_to_database("yello")
    # node_manager.nodes[3].add_to_database("hello")
    # # sleep()
    # while True:
    #     inp = input()
    #     if inp:
    #         if inp == 'r':
    #             r_inp = input()
    #             if r_inp:
    #                 if int(r_inp) in node_manager.nodes:
    #                     node_manager.remove_node(int(r_inp))
    #         elif inp == 'a':
    #             a_inp = input()
    #             if a_inp:
    #                 node_manager.add_node(list(map(int, list(a_inp))))
    #         elif int(inp) in node_manager.nodes:
    #             node_manager.nodes[int(inp)].add_to_database(inp + "ello")
