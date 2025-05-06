# app.py

"""
██████╗  █████╗ ███╗   ██╗████████╗████████╗
██╔════╝ ██╔══██╗████╗  ██║╚══██╔══╝╚══██╔══╝
██║  ███╗███████║██╔██╗ ██║   ██║      ██║   
██║   ██║██╔══██║██║╚██╗██║   ██║      ██║   
╚██████╔╝██║  ██║██║ ╚████║   ██║      ██║   
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   

██████╗██████╗  █████╗ ███████╗████████╗    
██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    
██║     ██████╔╝███████║█████╗     ██║       
██║     ██╔══██╗██╔══██║██╔══╝     ██║       
╚██████╗██║  ██║██║  ██║██║        ██║       
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝       

📊 **GanttCraft** - Turn task data into beautiful Gantt charts!
📁 Supports .txt, .csv, .xlsx
📤 Export as PNG, JPEG, PDF
🚀 Built by Parthiv Koli
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from datetime import datetime, timedelta

# Set page title and description
st.set_page_config(page_title="GanttCraft", page_icon="📊")
st.title("GanttCraft")
st.markdown("""
Upload a text, CSV, or Excel file containing task data to create a Gantt chart.  
Required columns: Task Name, Start Date, End Date.  
Optional columns:  
- Type (Task or Milestone)  
- Predecessor (Task ID of the preceding task for dependency arrows)  
- Category (for coloring tasks)  
**Date Format**: The app auto-detects various date formats (e.g., YYYY-MM-DD, MM/DD/YYYY, DD-MMM-YYYY). For best results, use consistent formats.  
Download your chart as a high-quality image or PDF!
""")

# File uploader
uploaded_file = st.file_uploader("Upload your file", type=["txt", "csv", "xlsx"], help="Supported formats: .txt (tab-separated), .csv, .xlsx")

if uploaded_file is not None:
    try:
        # Read the file based on its type
        if uploaded_file.type == "text/plain":
            data = pd.read_csv(uploaded_file, delimiter="\t")
        elif uploaded_file.type == "text/csv":
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            data = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type")
            st.stop()

        # Add an ID column if not present
        if "ID" not in data.columns:
            data["ID"] = range(1, len(data) + 1)

        # Display data preview
        st.subheader("Data Preview")
        st.dataframe(data, use_container_width=True)

        # Column selection
        columns = data.columns.tolist()
        col1, col2, col3 = st.columns(3)
        with col1:
            task_col = st.selectbox("Task Name Column", columns)
        with col2:
            start_col = st.selectbox("Start Date Column", columns)
        with col3:
            end_col = st.selectbox("End Date Column", columns)

        # Optional columns
        type_col = st.selectbox("Type Column (Task/Milestone, optional)", ["None"] + columns)
        type_col = None if type_col == "None" else type_col

        predecessor_col = st.selectbox("Predecessor Column (for dependency arrows, optional)", ["None"] + columns)
        predecessor_col = None if predecessor_col == "None" else predecessor_col

        color_col = st.selectbox("Color Tasks By (optional)", ["None"] + columns)
        color_col = None if color_col == "None" else color_col

        # Process date columns
        try:
            data[start_col] = pd.to_datetime(data[start_col], infer_datetime_format=True, errors='coerce')
            data[end_col] = pd.to_datetime(data[end_col], infer_datetime_format=True, errors='coerce')

            invalid_start = data[start_col].isna()
            invalid_end = data[end_col].isna()
            invalid_rows = data[invalid_start | invalid_end]

            if not invalid_rows.empty:
                st.warning(f"Some rows contain invalid or unparsable dates and will be excluded from the chart.")
                st.markdown("**Problematic Rows**:")
                st.dataframe(invalid_rows[[task_col, start_col, end_col]], use_container_width=True)
                st.markdown("**Tips**: Ensure dates are in recognizable formats (e.g., 2025-05-06, 05/06/2025, 06-May-2025) and check for non-date values or empty cells.")

            data = data[~(invalid_start | invalid_end)]

            if data.empty:
                st.error("No valid date data remains after filtering. Please check your date columns.")
                st.stop()

        except Exception as e:
            st.error(f"Failed to process dates: {str(e)}")
            st.markdown("**Tips**: Ensure the selected columns contain date-like values (e.g., 2025-05-06, 05/06/2025).")
            st.stop()

        # Create Gantt chart
        fig = go.Figure()

        # Colors for tasks (cycling through a palette)
        colors = ['#00CC96', '#636EFA', '#EF553B', '#AB63FA', '#FFA15A']
        task_colors = {}
        for idx, task in enumerate(data[task_col].unique()):
            task_colors[task] = colors[idx % len(colors)]

        # Separate tasks and milestones
        if type_col:
            tasks = data[data[type_col] == "Task"]
            milestones = data[data[type_col] == "Milestone"]
        else:
            tasks = data
            milestones = pd.DataFrame()

        # Add tasks as filled rectangles using Scatter with fill
        for idx, row in tasks.iterrows():
            task_name = row[task_col]
            start = row[start_col]
            end = row[end_col]
            # Create a rectangle with increased thickness
            y_position = task_name
            fig.add_trace(go.Scatter(
                x=[start, end, end, start, start],
                y=[y_position, y_position, y_position, y_position, y_position],
                fill="toself",
                fillcolor=task_colors.get(task_name, '#636EFA') if not color_col else row[color_col],
                line=dict(color='black', width=1),
                mode='lines',
                showlegend=False if not color_col else True,
                name=row[color_col] if color_col else None
            ))

        # Add milestones as diamond markers
        for idx, row in milestones.iterrows():
            fig.add_trace(go.Scatter(
                x=[row[start_col]],
                y=[row[task_col]],
                mode='markers',
                marker=dict(
                    symbol='diamond',
                    size=12,
                    color='black',
                    line=dict(color='black', width=1)
                ),
                showlegend=False
            ))

        # Add dependency arrows
        if predecessor_col:
            annotations = []
            for idx, row in data.iterrows():
                if pd.notna(row[predecessor_col]):
                    try:
                        pred_id = int(row[predecessor_col])
                        pred_row = data[data['ID'] == pred_id]
                        if not pred_row.empty:
                            pred_row = pred_row.iloc[0]
                            annotations.append(dict(
                                x=pred_row[end_col],
                                y=pred_row[task_col],
                                xref="x",
                                yref="y",
                                ax=row[start_col],
                                ay=row[task_col],
                                axref="x",
                                ayref="y",
                                showarrow=True,
                                arrowhead=2,
                                arrowsize=1,
                                arrowwidth=1.5,
                                arrowcolor="black"
                            ))
                    except (ValueError, TypeError):
                        continue
            fig.update_layout(annotations=annotations)

        # Calculate dynamic height and adjust based on number of tasks
        num_tasks = len(data[task_col].unique())
        chart_height = max(600, num_tasks * 80)  # Increased spacing per task

        # Determine timeline granularity based on date range
        date_range_days = (data[end_col].max() - data[start_col].min()).days
        if date_range_days > 90:  # More than 3 months
            tick_interval = 604800000.0  # Weekly ticks (7 days)
        elif date_range_days > 30:  # More than 1 month
            tick_interval = 172800000.0  # Bi-daily ticks (2 days)
        else:
            tick_interval = 86400000.0  # Daily ticks (1 day)

        # Customize layout
        fig.update_layout(
            xaxis=dict(
                title="Timeline",
                tickformat="%Y-%m-%d",
                dtick=tick_interval,
                gridcolor="lightgray",
                showgrid=True,
                range=[
                    data[start_col].min() - timedelta(days=1),
                    data[end_col].max() + timedelta(days=1)
                ],
                tickangle=45,
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="Tasks",
                autorange="reversed",
                tickfont=dict(size=14),  # Increased font size for readability
                showgrid=True,
                gridcolor="lightgray",
                title_font=dict(size=14),
                tickmode="array",
                tickvals=list(data[task_col].unique()),  # Ensure all task names are shown
                ticktext=[str(t)[:30] for t in data[task_col].unique()]  # Truncate long names
            ),
            font=dict(family="Arial", size=12, color="black"),
            title=dict(
                text="Project Gantt Chart",
                font=dict(size=24),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=150, r=50, t=80, b=80),  # Increased left margin for task names
            height=chart_height,
            showlegend=True if color_col else False,
            legend=dict(
                x=1.05,
                y=1,
                orientation="v",
                xanchor="left",
                yanchor="top"
            )
        )

        # Add today line
        today = datetime.today()
        if data[start_col].min() <= today <= data[end_col].max():
            fig.add_vline(x=today, line_width=2, line_dash="dash", line_color="red", annotation_text="Today", annotation_position="top")

        # Highlight weekends (optional, can be toggled off if too cluttered)
        min_date = data[start_col].min()
        max_date = data[end_col].max()
        current_date = min_date
        shapes = []
        while current_date <= max_date:
            if current_date.weekday() >= 5:  # Saturday or Sunday
                shapes.append(dict(
                    type="rect",
                    x0=current_date,
                    x1=current_date + timedelta(days=1),
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    fillcolor="rgba(200, 200, 200, 0.1)",  # Lighter shade to reduce clutter
                    line_width=0,
                    layer="below"
                ))
            current_date += timedelta(days=1)
        fig.update_layout(shapes=shapes)

        # Display chart
        st.subheader("Generated Gantt Chart")
        st.plotly_chart(fig, use_container_width=True)

        # Download options with custom dimensions
        st.subheader("Download Your Chart")
        st.markdown("Adjust the image dimensions for export (in pixels):")
        col_width, col_height = st.columns(2)
        with col_width:
            export_width = st.number_input("Width", min_value=800, max_value=4000, value=1920, step=100)
        with col_height:
            export_height = st.number_input("Height", min_value=600, max_value=3000, value=1080, step=100)

        formats = {"PNG": "png", "JPEG": "jpeg", "PDF": "pdf"}
        cols = st.columns(len(formats))
        for idx, (label, fmt) in enumerate(formats.items()):
            with cols[idx]:
                buf = io.BytesIO()
                fig.write_image(buf, format=fmt, engine="kaleido", width=export_width, height=export_height, scale=2)
                st.download_button(
                    label=f"Download {label}",
                    data=buf.getvalue(),
                    file_name=f"gantt_chart.{fmt}",
                    mime=f"image/{fmt}" if fmt != "pdf" else "application/pdf"
                )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.markdown("**Tips**: Ensure your file has valid data and recognizable date formats.")
else:
    st.info("Please upload a file to get started.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | Deployed on Streamlit Cloud")