from pathlib import Path
import datetime
def write_to_file(content: str) -> dict:

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")   

    filename = f'output/{timestamp}_generated_page.html'

    Path("output").mkdir(exist_ok=True)

    Path(filename).write_text(content)
    return {
        "status": "success",
        "message": f"Content written to {filename}"
    }