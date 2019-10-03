import plotly.graph_objects as go


fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
	    name="Name of Trace 1"
	    ))


fig.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
	    name="Name of Trace 2"
	    ))

fig.update_layout(
    title=go.layout.Title(
            text="Plot Title",
	            xref="paper",
		            x=0
			        ),
				    xaxis=go.layout.XAxis(
				            title=go.layout.xaxis.Title(
					                text="x Axis",
							            font=dict(
								                    family="Courier New, monospace",
										                    size=18,
												                    color="#7f7f7f"
														                )
								            )
					        ),
						    yaxis=go.layout.YAxis(
						            title=go.layout.yaxis.Title(
							                text="y Axis",
									            font=dict(
										                    family="Courier New, monospace",
												                    size=18,
														                    color="#7f7f7f"
																                )
										            )
							        )
						    )

fig.show()
