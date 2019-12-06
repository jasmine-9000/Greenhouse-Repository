#returns an array of tuples 

from matplotlib import pyplot as plt

available_styles = plt.style.available
form_data = []
for style in available_styles:
	form_choice = (style, style)
	form_data.append(form_choice)
print(form_data)
