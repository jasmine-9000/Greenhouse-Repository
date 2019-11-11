# imports
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates

# some RGB hex colors
all_devs_color_RGB_hex = '#444444'
py_devs_color_RGB_hex = '#5a7d9a'
js_devs_color_RGB_hex = '#adad3b'

def matplotlib_available_styles():
	available_styles = plt.style.available
	form_data = []
	for style in available_styles:
		form_choice = (style, style)
		form_data.append(form_choice)
	return form_data

def plot_graph(xrange, yrange, xlabel, ylabel, title, filepath, filename, style="fivethirtyeight", tightlayout=True):
	'''
		saves a graph to the filepath as the filename. You must specify the file format.
		
		plots a line graph based on the xrange and yrange data that you provide it.
		
	'''
	# use the style that's been passed in
	plt.style.use(style) 
	
	#plot the data passed in.
	plt.plot(xrange, yrange,color=all_devs_color_RGB_hex, label='line1') # plot the line.
	
	#label the x and y axes.
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	
	# add a title.
	plt.title(title)
	
	# add a tight layout upon user request)
	if tightlayout:
		plt.tight_layout()
	#save the figure to the filepath.
	plt.savefig(filepath + filename)
	# clear the figure.
	plt.clf()

def plot_pie_chart(slices, labels, colors, title, filepath, filename, style="fivethirtyeight",tightlayout=True, edgecolor="black"):
	"""
		plots a pie chart based on the slices that were passed in. It will calculate the percentages of each array slot, and draw a pie chart based on it.
	"""
	if labels:
		plt.pie(slices, labels=labels, colors=colors,wedgeprops={'edgecolor': edgecolor})
	else:
		plt.pie(slices, colors=colors)
		
	plt.title(title)
	if tightlayout:
		plt.tight_layout()
	plt.savefig(filepath + filename)
	plt.clf()



def plot_stack_plot(xrange, *yranges, xlabel="X-label", ylabels=[],title="stackplot", legendlocation="upper left", filepath="#", filename="#", style="fivethirtyeight", tightlayout=True):
	"""
			plots a stack plot. xrange is of dimension M.
			yranges is a list of arrays, all of dimension M. Default is an empty array.
			
			Title is optional for calling for this stackplot. default title is "stackplot".
			
			filepath and filename are optional, too. 
			
			legendlocation corresponds to loc. Look up matplotlib.legend.loc documentation for details. pass in legendlocation=(x,y) for coordinates to change it from upper left, for example. 
			
		
	"""
	plt.style.use(style) # use a passed_in style
	
	plt.stackplot(xrange, yranges, labels=ylabels) #plot a stackplot.
	plt.legend(loc=legendlocation) # add the legend.
	
	plt.title(title) #add a title.
	if tightlayout: # add a tight layout upon user request.
		plt.tight_layout()
	plt.savefig(filepath + filename) #save the figure to the filepath specified, then clear the figure.
	plt.clf()

def plot_histogram(data, bins, xlabel, ylabel, title, filepath, filename, style="fivethirtyeight", tightlayout=True,edgecolor="black",axvline=False, axvlinelabel='Median', axvvalue=None,axvcolor="orange"):
	'''
		plots a histogram, saves the figure to the filepath and as the filename. must specify the format in the filename.
		
		plots the data into the bins. will throw an error if the data doesn't fit into the bins.
		
		you can plot a single vertical line in the histogram. (e.g. the median of a dataset)
		If you want to do that, set axvline to True, pass in an axvvalue (mandatory), set a custom axvlinelabel string, and set an axvcolor.
		
	'''
	plt.style.use(style) #use a style.
	
	#plot your histogram.
	plt.hist(data, bins, edgecolor=edgecolor)
	# if you provided an axvline, label, and axvline (a highlighting bar somewhere in your histogram), plot it.
	if axvline:
		plt.axvline(axvvalue, color=axvcolor, label=axvlinelabel)
		plt.legend()
	
	plt.title(title) # add title, x and y labels.
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	
	
	if tightlayout: # add a tight layout upon user request.
		plt.tight_layout()
	plt.savefig(filepath + filename) # save the figure to the filepath, then clear the figure.
	plt.clf()

def plot_scatter_plot(xrange, yrange, xlabel, ylabel, title, filepath, filename, style="fivethirtyeight",dot_size=100,
	dot_color="green", linewidth=1, alpha=0.75, colorbar=False, colorbar_label_name="Color Bar Label", edgecolor="black", uselogscale=False,tightlayout=True):
	'''
		saves a graph to the filepath as the filename. You must specify the file format.
		
		dot_color can be an array, but it must be the same size as xrange and yrange.
		or else, it must be a string specifying what color you want it.
		default color is green.
		
		dot_size can be an array, but it must be the same size as xrange and yrange.
		or else, it must be an integer specifying what size you want it.
		default size is 100.
		
		you can either have a colorbar or not have a colorbar. Default is no colorbar. let's add it to the form.
		
		you can have a log scale by setting uselogscale=True.
		
		you can have a colorbar (only useful if you have an array of colors) by setting colorbar to True. Label it by passing in a colorbar_label_name="string". Replace "string" with whatever you want.
		
	'''
	plt.style.use(style) # use the style that you want.
	
 
	plt.scatter(xrange, yrange,s=dot_size, c=dot_color, edgecolor=edgecolor, linewidth=linewidth,alpha=alpha) #plot the scatter plot.
	
	# is capable of using a logarithmic scale upon user request.
	if uselogscale:
		plt.xscale('log')
		plt.yscale('log')
	
	plt.xlabel(xlabel) # add title, x and y label.
	plt.ylabel(ylabel)
	plt.title(title)
	
	if colorbar: # adds a colorbar upon user request.
		cbar = plt.colorbar()
		cbar.set_label(colorbar_label_name)
	
	if tightlayout: # adds a tight layout upon user request.
		plt.tight_layout()
	
	plt.savefig(filepath + filename) # saves the figure to the filepath, then clears the figure.
	plt.clf()
	
def plot_date(xrange, yrange, xlabel, ylabel, title, filepath, filename, style="fivethirtyeight", logarithmic_scale = False, tight_layout=True,linestyle='solid', marker=None, date_format="%H:%M"):
	'''
		plots a graph of dates.
		
		pass in a date_format (that will work with datetime.strftime()) to change the date format.
	'''
	
	plt.style.use(style) #use the style provided. default is fivethirtyeight.
	
	plt.plot_date(xrange, yrange, linestyle='solid') #plot the date graph.
	# autoformat the figure's x values (if they're dates).
	plt.gcf().autofmt_xdate()
	# create a mpl_dates Date Format to format dates with.
	d_format = mpl_dates.DateFormatter(date_format)
	# format the dates with d_format.
	plt.gca().xaxis.set_major_formatter(d_format)
	
	if logarithmic_scale: # set y scale 
		plt.yscale('log')
		
	plt.title(title) # add a title, x and y label.
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	
	plt.savefig(filepath + filename) # save the figure to the filepath, and clear the figure.
	plt.clf()