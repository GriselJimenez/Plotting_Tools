from __future__ import absolute_import, division, print_function
__author__ = 'Mostafa Hadavand'
__date__ = '2017-03-03'
__version__ = '1.00'


def logplot(z, var, cat=False, lw=2,varname='Variable', ax=None,
			aspect='auto',figsize=(2,12),lc='green',fontsize=12,yloc=1.02,colorlist=None, reversey=False,
			legend_fontsize=10,namelist=None, ylabel='Elevation (m)', out_kws=None):

	'''
	 A well log plot for both continuous and categorical variables. This plot handles one well log plot at a time and
	 the user can choose to generate subplots and pass the axes to this function if multiple well log plots are required.

    Parameters:
        z (Elevation/Depth or distance along the well): Tidy (long-form) 1D data
            where a single  column of the variable exists with each row is an
            observation. A pandas dataframe/series or numpy array can be passed.
        va (Variable being plotted): Tidy (long-form) 1D data where a single column of the variable exists with
            each row is an observation. A pandas dataframe/series or numpy array can be passed.
        lw (float): line width for log plot of a continuous variable
        figsize (tuple): Figure size (width, height)
        ax (mpl.axis): Existing matplotlib axis to plot the figure onto
        varname (str): title for the variable
        fontsize(float): fontsize for the tiltle that is name of the varible
        ylabel (str): Y-axis label
        lc (string): line color for the continuous variable
        aspect (str): Set a permissible aspect ratio of the image to pass to matplotlib.
        out_kws (): Optional dictionary of permissible keyword arguments to pass to
            :func:`gs.exportimg() <pygeostat.plotting.exportimg.exportimg>`
        colorlist(list): list of colors for all the unique codes of the categorical variable
        	example: colorlist=[(204, 0, 0), (255, 208, 0), (255, 147, 0),(0, 204, 0),(153, 153, 153)]
        legend_fontsize(float): fontsize for the legend plot rleated to the categorical codes.
        		set this parameter to 0 if you do not want to have a legend
        namelist(list): list with name for all the unique codes of the categorical variable
        	example: ['Sand','Breccia','SIHS','MIHS','MDST']
        yloc (float): location of the title of the plot
        reversey(bool): if true, the yaxis direction is set to reverse(applies to the cases that depth is plotted and not elevation)

    Returns:
        ax (ax): Matplotlib axis instance which contains the gridded figure

    Examples:
        A simple call:
        Bivariate KDE plot for 2 variables coming from Panad dataframe:
        >>> gs.logplot(DF['Z'],DF['phie'], cat=False, ax=ax, pltstyle=False, aspect='auto', varname='Porosity')

    .. codeauthor:: Mostafa Hadavand 2017-03-03

	'''

	from matplotlib.ticker import LinearLocator, FormatStrFormatter
	import matplotlib.patches as mpatches
	import matplotlib.pyplot as plt
	import numpy as np
	import pandas as pd



	#Sanity checks
	if not isinstance(z, (np.ndarray, np.generic, pd.Series)):
		raise ValueError("The parameter `z` must be a numpy array or a pandas series")
	if not isinstance(var, (np.ndarray, np.generic, pd.Series)):
		raise ValueError("The parameter `var` must be a numpy array or a pandas series")


	if not out_kws:
		out_kws = dict()

	if (ax is None):
		fig = plt.figure(figsize=figsize, dpi=250, facecolor='w', edgecolor='k')
		ax=fig.add_subplot(111)
	ax.set_aspect(aspect)

	DF=pd.DataFrame()
	DF['Z']=z
	DF['Var']=var
	DF.sort('Z',axis=0,ascending=True,inplace=True)
	DF.reset_index(inplace=True)

 	# Start of the plot
	if not (cat):
 		ax.plot(DF['Var'],DF['Z'],lw=lw,c=lc)
 		ax.set_title(varname,fontsize=fontsize,y=yloc)
 		ax.set_ylabel(ylabel,fontsize=fontsize)
 		ax.set_xlim([min(DF['Var']), max(DF['Var'])])
 		ax.set_ylim([min(DF['Z']), max(DF['Z'])])
 		ax.set_xticks(np.linspace(min(DF['Var']), max(DF['Var']), 2))
 		ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
 		ax.xaxis.set_label_position('top')
 		ax.xaxis.set_ticks_position('top')

	else:
		ncat=len(np.unique(DF['Var']))
		DataNum=len(DF)
		width=1.0

		if colorlist is None:
			colorlist=[]
			for i in range(ncat):
				colorlist.append((np.random.randint(0,255,1)[0],np.random.randint(0,255,1)[0],np.random.randint(0,255,1)[0]))

		if (len(colorlist)!=ncat):
			raise ValueError("Wrong number of colors in the colorlist!")


		if namelist is None:
			namelist=[]
			for i in range(ncat):
				string='Category Code %i'%(i+1)
				namelist.append(string)

		if (len(namelist)!=ncat):
			raise ValueError("Wrong number of names in the namelist!")

		my_colors= tuple(tuple(i / 255.0 for i in inner) for inner in colorlist)

		ind=np.arange(1)
		for i in range (1,DataNum):
			Pbar = ax.bar(ind, DF['Z'][i]-DF['Z'][i-1], width, color=my_colors[int(DF['Var'][i]-1)],edgecolor=my_colors[int(DF['Var'][i])-1],bottom=DF['Z'][i-1])
			ax.set_title(varname,fontsize=fontsize,y=yloc)
			ax.set_ylabel(ylabel,fontsize=fontsize)
			ax.set_ylim([min(DF['Z']), max(DF['Z'])])
			ax.set_xlim([0,0.5])
			ax.xaxis.set_label_position('top')
			ax.get_xaxis().set_visible(False)

		Patch_list=[]
		for i in range(ncat):
			Patch_list.append(mpatches.Patch(color=my_colors[i], label=namelist[i]))

		if (legend_fontsize>0):
			ax.legend(handles=Patch_list,loc='upper left', bbox_to_anchor=(1, 1),fontsize=legend_fontsize)


	if (reversey):
		plt.gca().invert_yaxis()






	return ax
