import dash_interactive_graphviz
import dash
import networkx as nx
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import node_manager

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
                html.H3("selected node id:"),
                html.Div(id="node_id"),

                html.H3("log_state:"),
                html.Div(id="log_state"),

                html.H3("Database:"),
                dcc.Textarea(
                    id="database",
                    style=dict(flexGrow=0.5, position="relative")
                ),

                html.H3("enter data to add:"),
                dcc.Textarea(
                    id="data_to_add",
                    style=dict(height=20, position="relative")
                ),
                html.Button("add_data", id="add_data_btn", style={"margin-bottom": "15px"}),

                html.H3("enter new neighbors:"),
                dcc.Textarea(
                    id="new_neighbors",
                    style=dict(height=20, position="relative")
                ),
                html.Button("change_neighbors", id="change_neighbors_btn", style={"margin-bottom": "15px"}),

                html.H3("node to add:", style={"margin-bottom": "1px"}),
                html.H3("enter node neighbors ex. (0, 1, 2)"),
                dcc.Textarea(
                    id="node_neighbors",
                    style=dict(height=20, position="relative")
                ),

                html.Button("add_node", id="add_btn", n_clicks=0, style={"margin-bottom": "30px"}),
                html.Button("remove_node", id="remove_btn", n_clicks=0, style={"margin-bottom": "15px"}),
            ],
            style=dict(display="flex", flexDirection="column"),
        ),
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)


@app.callback(Output("gv", "dot_source"),
              Input("add_btn", "n_clicks"), Input("remove_btn", "n_clicks"), Input("change_neighbors_btn", "n_clicks"),
              State("node_neighbors", "value"), State("node_id", "children"), State("new_neighbors", "value"))
def manage_nodes(_, __, ___, node_neighbors, node_id, new_neighbors):
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_id == "remove_btn":
        if node_id:
            node_manager.remove_node(int(node_id["props"]["children"]), dot)
    elif button_id == "add_btn":
        if node_neighbors:
            node_manager.add_node(list(map(int, node_neighbors.split(","))), dot)
        else:
            node_manager.add_node([], dot)
    elif button_id == "change_neighbors_btn":
        if node_id:
            if new_neighbors:
                node_manager.change_neighbors(int(node_id["props"]["children"]), list(map(int, new_neighbors.split(","))), dot)
            else:
                node_manager.change_neighbors(int(node_id["props"]["children"]), list(), dot)

    return str(nx.drawing.nx_pydot.to_pydot(dot))


@app.callback(Output("node_id", "children"), Output("database", "value"), Output("log_state", "children"),
              Output("gv", "selected_node"),
              Input("gv", "selected_node"), Input("add_data_btn", "n_clicks"),
              State("data_to_add", "value"), State("node_id", "children"))
def manage_node(selected_node, _, data, node_id):
    if selected_node is None:
        raise dash.exceptions.PreventUpdate

    if selected_node == -1:
        node_id = node_id["props"]["children"]
        node_manager.nodes[int(node_id)].add_to_database(data)
        selected_node = node_id

    return html.Div(selected_node), str(node_manager.nodes[int(selected_node)].database.data), \
        html.Div(str(node_manager.nodes[int(selected_node)].log_state)), -1


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

