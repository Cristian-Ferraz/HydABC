import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cobra
import plotly.express as px
from PIL import Image
import plotly.io as pio
import straindesign as sd
from ipywidgets import interact, interactive
from ipywidgets import FloatSlider, FloatLogSlider
from matplotlib.patches import Patch

# This function returns a data frame containing the principal production and consumption fluxes for any metabolite in a given model.

"""The threshold parameter defines the minimum contribution required for a enzyme to be included in the visualization of metabolite 
production or consumption."""

def metabolite_df(model,solution,metabolite,threshold=0):
    df_prod = model.metabolites.get_by_id(metabolite).summary(solution).producing_flux
    df_prod = df_prod.loc[:,['flux','percent']]
    
    df_cons = model.metabolites.get_by_id(metabolite).summary(solution).consuming_flux
    df_cons = df_cons.loc[:,['flux','percent']]
    
    if threshold !=0:
        df_cons = df_cons.loc[df_cons['percent'] > threshold]
        df_prod = df_prod.loc[df_prod['percent'] > threshold]
        
    frames = [df_prod, df_cons]
    result = pd.concat(frames)
    result = result.sort_values(by=['flux'])

    return result


# This function generates a bar plot showing the consumption and production fluxes of a specified metabolite.

def plot_df(df, title, y_limit, biomass_value, rot=0, ax=None):

    fig_created = False
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,4))
        fig_created = True
        
    colors = ["indigo" if val > 0 else "cyan" for val in df['flux']]
    bars = ax.bar(df.index, df['flux'], color=colors, edgecolor='black',width=0.8)
    
    
    colors1 = {'Consumption':'cyan', 'Production':'indigo'}         
    labels = list(colors1.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors1[label]) for label in labels]
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2,
                yval + 0.1 if yval > 0 else yval - 0.1,
                f'{yval:.2f}',
                ha='center',
                va='bottom' if yval > 0 else 'top',
                fontsize=9)
        
    ax.text(
        0.99, 0.05,
        "Biomass: "+str(biomass_value),         
        ha='right', va='bottom',    
        transform=ax.transAxes,     
        fontsize=9, color="black",
        weight = 'bold',
        bbox=dict(
            boxstyle="round,pad=0.3",   
            facecolor="white",          
            edgecolor="black",          
            alpha=0.8                   
            )
        )

    index_list = [i[0:-3] for i in df.index]
    
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(np.arange(len(df)), index_list, rotation=rot, fontsize=10)
    ax.set_ylim(y_limit)
    ax.set_ylabel("Flux [mmol gDW⁻¹ h⁻¹]", weight='bold')
    ax.set_yticklabels([])
    ax.set_title(title, weight='bold')
    ax.legend(handles, labels)
    ax.grid(linestyle='dashed')
    ax.set_axisbelow(True)
    
    if fig_created:
        fig.tight_layout()


# The parameters of the function are the model, the list of enzymes.
def Max(model,enzyme):
    
    bound = 0.0
            
    while True:
        with model:
            model.reactions.get_by_id(enzyme).bounds = (bound,bound)
            solution = model.optimize()

            # if solution is infeasible, return the last value that generates a feasible result
            if solution.objective_value is None:
                bound_max = bound-0.01
                break
                        
            # If there is a solution, continues enhancing/decreasing the flux 
            else:
                bound+=0.01

    return bound_max

def interactive_changes(model, enzyme, initial_flux, enzyme_max):

    r_imp = ['PDH_fw','PPC_fw','CS_fw','ACONTa_fw','ACONTa_bw',
             'ACONTb_fw','ACONTb_bw','ICDHyr_fw','ICDHyr_bw',
             'AKGDH_fw','SUCOAS_fw','SUCOAS_bw','FUM_fw','FUM_bw',
             'FRD2_fw','ICL_fw','ICL_bw','MALS_fw','MDH_fw', 'MDH_bw']

    r_imp_final = []

    for i in r_imp:
        if i != enzyme:
            r_imp_final.append(i)
    
    @interact (
        slide = (0.0,enzyme_max,0.001)
    )
    
    def changes(slide = initial_flux):
    
        dict_aux = {l:[] for l in r_imp_final}
        dict_aux['NADH'] = []
        dict_aux['Biomass'] = []
    
        with model as m:
            
            try:
                if slide != initial_flux:
                    m.reactions.get_by_id(enzyme).bounds = (slide,slide)
                
                solution = m.optimize()
        
                if solution.objective_value is not None:
                        
                    for reaction in r_imp_final:
                        dict_aux[reaction].append(solution.fluxes[reaction])
            
                    dict_aux['Biomass'].append(solution.objective_value)
                    dict_aux['NADH'].append(sum(m.metabolites.get_by_id('nadh_c').summary(solution).producing_flux['flux']))
            
                df = pd.DataFrame(dict_aux)
                display(df)
                
            except Exception as e:
                print(f"Error: {e}")


# This function evaluates NADH and biomass synthesis in front of variantions on specific enzymes fluxes

#def nadh_hyd(model,reaction,upper,step,ko_list=None):
def nadh_hyd(model,reaction,step,ko_list=None):

    # model: model to be analyzed
    # reaction: list with reactions that will have fluxes changed over a range
    # upper: upper limit to constrain reaction flux
    # step: in wich steps the range of flux will vary
    # ko_list: optional list of enzymes to knockout

    upper = max(reaction.values())
    first = True
    
    nadh_bio = {'NADH Total':[], 'Biomass':[]}

    
    h2_dict = {"Biomass": [], "H2": [], "Glucose": []}
    
    for i in np.arange(0.0,upper,step):
        try:
            with model:
                if ko_list is not None:
                    for k in ko_list:
                        model.reactions.get_by_id(k).bounds = (0,0)

                for r in reaction.keys():
                    if i <= reaction[r]:
                        model.reactions.get_by_id(r).bounds = (i,i)
                    else:
                        model.reactions.get_by_id(r).bounds = (reaction[r],reaction[r])

                solution = model.optimize()

                if solution.objective_value is not None:

                    if first:
                        results = {i:[] for i in model.metabolites.get_by_id('nadh_c').summary(solution).consuming_flux['flux'].index}
                        first = False

                    nadh_bio['NADH Total'].append(sum(model.metabolites.get_by_id('nadh_c').summary(solution).producing_flux['flux']))
                    nadh_bio['Biomass'].append(solution.objective_value)
                        
                    #h2_dict['H2'].append(sum(model.metabolites.get_by_id('h2_c').summary(solution).producing_flux['flux']))
                    h2_dict['H2'].append(solution.fluxes['EX_h2_e_fw'])
                    h2_dict['Biomass'].append(solution.objective_value)
                    h2_dict['Glucose'].append(solution.fluxes['EX_glc__D_e_bw'])

                    for j in results:
                        results[j].append(abs(model.metabolites.get_by_id('nadh_c').summary(solution).consuming_flux['flux'][j]))
            
        except:
            continue

    if first:
        return 0

    else:
        return (pd.DataFrame(nadh_bio | results), h2_dict)

# Function for heat map generation (adapted from Part_6)

def enzyme_variation(solution_control, solution_scenario, enzymes_number,name):

    # solution_control = solution fluxes of control model
    # solution_scenario = calculated fluxes from solution of the scenario to be analized
    # enzymes_number = threshold of enzymes that will be shown
    # name = name of the scenario

    # log2 FC calculation
    df_FC = (solution_scenario.fluxes + 0.01) / (solution_control.fluxes + 0.01)
    df_log_FC = np.log2(df_FC)
    
    df_final = pd.DataFrame(df_log_FC)
    df_final = df_final.sort_values(by='fluxes',key=abs,ascending=False).iloc[0:enzymes_number]
    df_final = df_final.sort_values(by='fluxes',ascending=False).iloc[0:20]
    df_final.rename(columns={'fluxes': name}, inplace=True)

    return df_final


# Function for PFOR and OGOR flux visualization in response of an specific enzyme flux
def pfor_ogor(model,enzyme_over,enzyme_het,upper,step,title):

    # model: model to be analyzed
    # enzyme_over: enzyme present on the model that will have flux modified
    # enzyme_het: enzyme to have flux evaluates in response of enzyme_over modifications
    # upper: upper bound for flux restriction in enzyme_over range of modification
    # step: in which step the range of flux for enzyme_over modification will vary
    # title: title of the generated graph
    
    results = {enzyme_over:[], enzyme_het:[]}
    for i in np.arange(0.0,upper,step):
        with model:
            model.reactions.get_by_id(enzyme_over).bounds = (i,i)
            solution = model.optimize()
            
            results[enzyme_over].append(i)
            results[enzyme_het].append(solution.fluxes[enzyme_het])
    
    df = pd.DataFrame(results)

    fig, ax = plt.subplots(layout='constrained')

    
    ax.plot(df[enzyme_over],df[enzyme_het],'-.',color='b')
    
    ax.set_ylabel(enzyme_het[:-3] + " [mmol gDW⁻¹ h⁻¹]")
    ax.set_xlabel(enzyme_over[:-3] + " [mmol gDW⁻¹ h⁻¹]")
    ax.set_title(title,weight='bold')

    path = '../Images/'
    file = title + '.png'
    
    fig.savefig(path+file,dpi=1200)

def plot_lines(df, colors, form, title, legend, ax=None):

    # df: data frame with NADH/biomass production and the main enzymes responsible for NADH consumption
    # colors: colors of the lines
    # form: format of the lines to be ploted
    # ax: axis to plot the graph
    
    fig_created = False
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,4))
        fig_created = True
    
    ax_aux = ax.twinx()

    for i,j,k in zip(df.columns[1:], colors, form):
        if i == 'Biomass':
            ax_aux.plot(df['NADH Total'],df[i],k,label=i,color=j)
    
        else:
            ax.plot(df['NADH Total'],df[i],k,label=i[:-3],color=j)
    
    ax_aux.set_ylabel("Biomass [h⁻¹]")
    ax.set_xlabel("Total NADH [mmol gDW⁻¹ h⁻¹]")
    ax.set_ylabel("Flux [mmol gDW⁻¹ h⁻¹]")
    ax.set_title(title, weight='bold')
    
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax_aux.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2,loc=legend)

    if fig_created:
        fig.tight_layout()

# function to plot the pie graph of H+ production and consumption on both scenarios
def pie_graph(df,title):
    
    df['enzymes'] = [i[0:-3] for i in df.index]
    df.reset_index(inplace=True)
    df['behavior'] = df['flux'].apply(lambda x: 'consumption' if x < 0 else 'production')
    df.drop(['index'],axis=1,inplace=True)

    fig = px.sunburst(df, path=['behavior', 'enzymes'], values='percent',
                      color='flux', 
                      color_continuous_scale='RdBu',
                      title=title)
    
    fig.show(config={'toImageButtonOptions': {'format': 'png', 'height': 800, 'width': 1000, 'scale': 4}})

# Function to find H2 production in the data frame corresponding to a specific growth rate
# returns the H2 production (total flux and yield) corresponding to the closest given biomass value on the data frame, along with its respective index 
def near(df,column,target):
    
    # column: data frame column used as the reference for the search
    # target: value to be matched to the closest entry in the selected column
    
    differences = np.abs(df[column] - target)
    nearest_index = differences.argsort()[0]
    h2 = df['H2'].iloc[nearest_index]
    glc = df['Glucose'].iloc[nearest_index]

    y = h2/glc
    
    return (h2,y,nearest_index)



def mcs(model,h2,const):

    dict_aux = {'H2 Yield':[],'Solution': []}
    
    while True:

        ko_cost = {g.id:1 for g in model.reactions}

        sols = sd.compute_strain_designs(model,
                                 sd_modules = const,
                                 time_limit = 300,
                                 max_solutions = 1,
                                 ko_cost = ko_cost,
                                 max_cost = 10,
                                 solution_approach = sd.names.BEST,
                                 gene_kos = True)

        if len(sols.reaction_sd) != 0:
            dict_aux['H2 Yield'].append(h2)
            dict_aux['Solution'].append(sols)
            h2 += 0.1
            sup = [f'EX_h2_e_fw - {h2} EX_glc__D_e_bw <= 0', 'EX_glc__D_e_bw >= 0.1']
            const[0] = sd.SDModule(model,sd.names.SUPPRESS, constraints=sup)
                
        else:
            break
        
    return dict_aux


def plot_growth_couple(model,dict_conditions,dict_colors,file_name=None,ax=None):
        
    if ax is None:
        fig, ax = plt.subplots(figsize=(6,4))

    # backgorund graph
    datapoints, triang, plot1 = sd.plot_flux_space(model,
                                                   dict_conditions['Background'],
                                                   show=False,
                                                   ax=ax);
    plot1.set_facecolor(dict_colors['Background'])
    plot1.set_edgecolor(dict_colors['Background'])
    
    # module to protect
    _,          _,      plot2 = sd.plot_flux_space(model,
                                                   dict_conditions['Background'],
                                                   constraints=dict_conditions['Protect'],
                                                   show=False,
                                                   ax=ax);
    plot2.set_facecolor(dict_colors['Protect'])
    plot2.set_edgecolor(dict_colors['Protect'])
    
    
    # module to suppress
    _,          _,      plot3 = sd.plot_flux_space(model,
                                                   dict_conditions['Background'],
                                                   constraints=dict_conditions['Suppress'],
                                                   show=False,
                                                   ax=ax);
    plot3.set_facecolor(dict_colors['Suppress'])
    plot3.set_edgecolor(dict_colors['Suppress'])
    
    if dict_conditions['Knockouts'] == 0:
        plot3.axes.set_xlim(0, 1.05*max([a[0] for a in datapoints]))
        plot3.axes.set_ylim(0, 1.05*max([a[1] for a in datapoints]))

        if file_name != None:
            save_name = '../Images/' + file_name
            plt.savefig(save_name,dpi=1200)

        plt.show()

    else:
        # plotting designed strain
        _,          _,      plot4 = sd.plot_flux_space(model,
                                                       dict_conditions['Background'],
                                                       constraints=dict_conditions['Knockouts'],
                                                       show=False,
                                                       ax=ax);
        plot4.set_facecolor(dict_colors['Knockouts'])
        plot4.set_edgecolor(dict_colors['Knockouts'])
    
        plot4.axes.set_xlim(0, 1.05*max([a[0] for a in datapoints]))
        plot4.axes.set_ylim(0, 1.05*max([a[1] for a in datapoints]))
        
        if file_name != None:
            save_name = '../Images/' + file_name
            plt.savefig(save_name,dpi=1200)
        
        plt.show()


def plot_yields(dict_h2, dict_NADH, legend, title, ax):
    dict_h2['NADH'] = dict_NADH['NADH Total']
    dict_h2['Biomass'] = dict_NADH['Biomass']

    df_h2 = pd.DataFrame(dict_h2)
    df_h2['Yield'] = df_h2['H2']/df_h2['Glucose']
    df_h2 = df_h2.sort_values(by = 'NADH', ascending=True)

    ax2 = ax.twinx()
    
    ax.plot(df_h2['NADH'],df_h2['Biomass'], '.-', color= 'g', label='Biomass')
    
    ax2.plot(df_h2['NADH'],df_h2['Yield'], 'x-', color= 'b', label='Yield')
    
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2,loc=legend)

    ax.set_xlabel("Total NADH [mmol gDW⁻¹ h⁻¹]")
    ax.set_ylabel("Biomass [h⁻¹]")
    ax2.set_ylabel("H₂ Yield [mol/mol glc]")
    ax.set_title(title, weight='bold')

def boxplot(data, colors, title, yaxis, tick_label, patterns, hor, locs, ax=None):

    if ax is None:
        fig, ax = plt.subplots(figsize=(10,6))
    
    boxes = ax.boxplot(data, 
                       patch_artist=True, 
                       tick_labels=tick_label, 
                       showfliers=False, 
                       medianprops=dict(color='black')) 

    for patch, color in zip(boxes['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')

    for patch, pattern in zip(boxes['boxes'], patterns):
        patch.set_hatch(pattern)
    
    color_handles = [
        Patch(facecolor='blue', edgecolor='black', label='PPC+'),
        Patch(facecolor='red', edgecolor='black', label='CS+'),
        Patch(facecolor='yellow', edgecolor='black', label='OGOR+'),
        Patch(facecolor='green', edgecolor='black', label='OGOR+/PPC+')
    ]

    legend1 = ax.legend(handles=color_handles,
                        loc=locs[0],
                        title="Modification")
    
    pattern_handles = [
        Patch(facecolor='white', edgecolor='black', hatch='.', label='PFOR'),
        Patch(facecolor='white', edgecolor='black', hatch='*', label='OGOR'),
        Patch(facecolor='white', edgecolor='black', hatch='/', label='PFOR/OGOR')
    ]

    legend2 = ax.legend(handles=pattern_handles,
                        loc=locs[1],
                        title="Models")

    ax.add_artist(legend1)
    ax.set_ylabel(yaxis, weight='bold')
    ax.grid(linestyle='dashed')
    ax.set_title(title, weight='bold')
    ax.axhline(y=hor, color='green', linestyle='--')

    save = '../Images/' + title + '.png'
    
    fig.savefig(save,dpi=1200)