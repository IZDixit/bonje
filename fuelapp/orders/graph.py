# This is the file, where all graphing functions will exist.

# UserWarning:
# Starting a Matplotlib GUI outside of the main thread will likely fail.
# We now need to use a non-GUI backend
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from io import BytesIO
import base64



# This will be used by the Manager Dashboard in views.py
# Display customer orders
def create_customer_chart(labels, data):
    fig, ax = plt.subplots()
    ax.bar(labels, data, color='teal')
    ax.set_xlabel('Customer Username')
    ax.set_ylabel('Total Quantity')
    ax.set_title('Customer Order Totals')

    # Save the plot to a BytesIO object and encode it in base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig) # Closing figure to free memory.
    return img_str