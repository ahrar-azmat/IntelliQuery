import matplotlib.pyplot as plt
import io
import base64

def create_graph(data, title="Graph", xlabel="X-axis", ylabel="Y-axis"):
    plt.figure(figsize=(10,6))
    plt.bar(data.keys(), data.values())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graph_base64 = base64.b64encode(image_png).decode('utf-8')
    return graph_base64
