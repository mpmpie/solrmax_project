import numpy as np
import matplotlib.pyplot as plt
import panel as pn

# Initialize Panel extension
pn.extension()

# Create a Panel layout
dashboard = pn.Column()

# Serve the dashboard
dashboard.servable()