# Your existing libraries (pickle, Llama modules)

import dash_html_components as html

from dash import State
from dash.dependencies import Input, Output
from dash_table import DataTable

from dashboard import DASHBOARD_STYLE
from data.data import load_sample_data
from model.model import (
    create_dataframe_engine,
    create_img,
    load_embedding_model,
    load_llm_model,
    load_codellama,
    load_service,
)
from dashboard.style import create_app
from os import getenv

openai_api_key = getenv("OPENAI_API_KEY")

df = load_sample_data()

if openai_api_key is None:
    embed_model = load_embedding_model()
    llm_code_model = load_codellama()
    llm_model = load_llm_model()
    load_service(llm_code_model, embed_model)

query_engine = create_dataframe_engine(df)

app = create_app()


@app.callback(
    [
        Output("data-container", "style"),
        Output("output-container", "style"),
        Output("prompt-container", "style"),
        Output("submit-button", "style"),
        Output(component_id="submit-button", component_property="n_clicks"),
    ],
    Input("tabs", "value"),
)
def show_hide_content(selected_tab):
    if selected_tab == "tab-data":
        data_container_style = DASHBOARD_STYLE["data-container"]["style"]
        if "display" in data_container_style:
            data_container_style.pop("display")
        return (
            data_container_style,
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            0,
        )
    elif selected_tab == "tab-data-insight":
        updated_style = {}
        for container_key in [
            "output-container",
            "prompt-container",
            "submit-button",
        ]:
            updated_style[container_key] = DASHBOARD_STYLE[container_key]["style"]
            if "display" in updated_style[container_key]:
                updated_style[container_key].pop("display")
        return [
            {"display": "none"},
            updated_style["output-container"],
            updated_style["prompt-container"],
            updated_style["submit-button"],
            0,
        ]
    elif selected_tab == "tab-about":
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            0,
        )
    else:
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            0,
        )


@app.callback(Output("data-container", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-data":
        return html.Div(
            [
                DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("records"),
                    filter_action="native",
                    fill_width=False,
                    style_data=DASHBOARD_STYLE["data"]["style"]["cell"],
                    style_header=DASHBOARD_STYLE["data"]["style"]["header"],
                    style_table=DASHBOARD_STYLE["data"]["style"]["table"],
                ),
            ]
        )


@app.callback(
    [
        Output(component_id="output-container", component_property="children"),
        Output(
            component_id="pandas-instruction-container", component_property="children"
        ),
    ],
    Input("tabs", "value"),
    Input(component_id="submit-button", component_property="n_clicks"),
    [
        State(component_id="prompt-container", component_property="value"),
        State(component_id="output-container", component_property="children"),
    ],
    prevent_initial_call=True,
)
def update_output(tab, n_clicks, prompt, current_output):

    if tab == "tab-data-insight":
        if n_clicks > 0:
            if prompt:
                response = query_engine.query(prompt)
                pandas_instruction_str = response.metadata["pandas_instruction_str"]

                if "plot" in pandas_instruction_str.lower():
                    image_src = create_img(df, pandas_instruction_str)

                    return [
                        html.Div(
                            [
                                current_output,
                                html.P(
                                    f"Q: {prompt}",
                                    style=DASHBOARD_STYLE["prompt"]["style"],
                                ),
                                html.Div(
                                    [html.Img(src=image_src)],
                                    style=DASHBOARD_STYLE["image"]["style"],
                                ),
                            ]
                        ),
                        pandas_instruction_str,
                    ]
                else:
                    results = response.response
                    return [
                        html.Div(
                            [
                                current_output,
                                html.P(
                                    f"Q: {prompt}",
                                    style=DASHBOARD_STYLE["prompt"]["style"],
                                ),
                                html.Pre(
                                    results,
                                    style=DASHBOARD_STYLE["answer"]["style"],
                                ),
                            ]
                        ),
                        pandas_instruction_str,
                    ]
            else:
                return [html.Div("Please enter a prompt."), None]
        else:
            return [None, None]
    else:
        return [None, None]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
