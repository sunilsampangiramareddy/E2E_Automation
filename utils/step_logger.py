import os
import webbrowser
from datetime import datetime
from pathlib import Path

class StepLogger:
    def __init__(self, report_dir="report", screenshot_dir="screenshots"):
        self.steps = []
        self.report_dir = Path(report_dir)
        self.screenshot_dir = Path(screenshot_dir)

        # Create directories if they don't exist
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def log_step(self, step_name, page):
        """
        Logs a test step, captures a screenshot, and stores the step details.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.screenshot_dir / f"{step_name}_{timestamp}.png"
        try:
            # Capture screenshot
            page.screenshot(path=str(screenshot_path))
            print(f"Screenshot saved at: {screenshot_path}")
        except Exception as e:
            print(f"Error capturing screenshot for step '{step_name}': {e}")
            screenshot_path = "Screenshot failed"

        # Save relative path for the HTML report
        relative_screenshot_path = os.path.relpath(screenshot_path, self.report_dir)
        self.steps.append({
            "step": step_name,
            "screenshot": relative_screenshot_path
        })

    def generate_html_report(self, output_file=None, title=None):
        """
        Generates an HTML report with all logged steps and their screenshots.
        If no output_file is provided, a default name with the current date and time is generated.
        If output_file is provided, '_Full_Report' is automatically appended to the name.
        The title of the report is automatically derived from the report name if not explicitly provided.
        """
        # Append timestamp to the report name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_file is None:
            # Default report name
            output_file = f"Test_Report_{timestamp}.html"
        else:
            # Automatically append '_Full_Report' if not already included
            if "_Full_Report" not in output_file:
                output_file += "_Full_Report"
            # Ensure the file name ends with .html and append timestamp
            if not output_file.endswith(".html"):
                output_file += ".html"
            output_file = f"{os.path.splitext(output_file)[0]}_{timestamp}.html"

        # Derive the title from the report name if not explicitly provided
        if title is None:
            title = os.path.splitext(os.path.basename(output_file))[0]  # Remove the .html extension

        # Ensure the report is saved in the report directory
        output_file = self.report_dir / output_file

        html = f"""
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                img {{ border: 1px solid #ddd; margin: 10px 0; max-width: 300px; }} /* Reduced size */
            </style>
        </head>
        <body>
            <h1>{title}</h1>
        """
        for step in self.steps:
            html += f"<h2>{step['step']}</h2>"
            if step['screenshot'] != "Screenshot failed":
                html += f"<img src='{step['screenshot']}' style='width:300px;'/>"  # Reduced size
            else:
                html += "<p>Screenshot not available</p>"
        html += "</body></html>"

        # Write the HTML content to the output file
        with open(output_file, "w") as f:
            f.write(html)

        print(f"Report generated: {output_file}")
        webbrowser.open(str(output_file))
