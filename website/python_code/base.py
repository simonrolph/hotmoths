import os
import random
import pandas as pd
import numpy as np

# we want to generate the html for the website from the template
# and the database that we will have created in data/stats_for_page.csv
# and data/text_from_facts.csv 

templatefile = '../index.html'
statsfile = '../../data/cleaned_stats_for_page.csv'
textfile = '../../data/text_from_facts2.csv'
tstartline = 63 # <div class="tinder-cards" id="tindercards"> line
tendline   = 91 # </div> of last tinder card line 

# 1) read in the template
with open(templatefile, 'r') as tfile:
	filedata = tfile.readlines()

# 2) Extract out the beginning and end
filestart = filedata[:tstartline]
fileend   = filedata[tendline:]

# 3) Extract out the template bit to edit
#    Or just hardcode it here
template = \
'''
   <div class="tinder--card">
      <img src="IMAGEURL"
      width="500"
      height="150"
      title=IMGATT/>
      <h3>MOTHNAME</h3>
      <p><a id="locationtext"><i class="fa fa-map-marker"></i> <span id="moth-dist-1">?</span> km from your location</a></p>
      <p>FACT1</p>
      <p>FACT2</p>
      <p>FACT3</p>
      <p>FACT4</p>
      <p>FACT5</p>
      <p>FACT6</p>

    </div>
'''

# 4) Read in the data from the csv files
stats = pd.read_csv(statsfile)
texts = pd.read_csv(textfile, encoding='ANSI')
nmoths = stats.shape[0]

residence_texts = texts[texts['feature']=='resident']
residence_texts_t = residence_texts[residence_texts['value']=='TRUE']['text']
residence_texts_f = residence_texts[residence_texts['value']=='FALSE']['text']
diurnal_texts   = texts[texts['feature']=='diurnal']
diurnal_texts_t = diurnal_texts[diurnal_texts['value']=='TRUE']['text']
diurnal_texts_f = diurnal_texts[diurnal_texts['value']=='FALSE']['text']
abundance_texts   = texts[texts['feature']=='widespread']
abundance_texts_t = abundance_texts[abundance_texts['value']=='TRUE']['text']
abundance_texts_f = abundance_texts[abundance_texts['value']=='FALSE']['text']
mass_texts   = texts[texts['feature']=='big']
mass_texts_t = mass_texts[mass_texts['value']=='TRUE']['text']
mass_texts_f = mass_texts[mass_texts['value']=='FALSE']['text']
pick_texts   = texts[texts['feature']=='pickiness']
pick_texts_o = pick_texts[pick_texts['value']=='O']['text']
pick_texts_p = pick_texts[pick_texts['value']=='P']['text']
pick_texts_m = pick_texts[pick_texts['value']=='M']['text']

newtemplates = []
for moth in range(0, nmoths):
    mothname   = stats['common_name'].iloc[moth]
    sciname    = stats['sci_name'].iloc[moth]
    mass       = stats['big'].iloc[moth] # T or F
    diurnal    = stats['diurnal'].iloc[moth] # T or F
    abundance  = stats['widespread'].iloc[moth] # T or F
    plants     = stats['hostplant'].iloc[moth]
    resident   = stats['resident'].iloc[moth] # T or F
    pickiness  = stats['pickiness'].iloc[moth] # 3 options (P,O,M)
    imgurl     = stats['image'].iloc[moth]
    imgatt     = stats['att'].iloc[moth]
    
    # 5) Edit template with data from step 4
    newtemplate = template.replace('MOTHNAME', mothname)
    if pd.isna(plants):
        newtemplate = newtemplate.replace('<p>FACT1</p>', '')
    else:
        newtemplate = newtemplate.replace('FACT1', 'Fave plants: ' + str(plants))
    
    # resident
    if pd.isna(resident):
        newtemplate = newtemplate.replace('<p>FACT2</p>', '')
    else:
        if resident == True:
            rint = np.random.randint(0, residence_texts_t.shape[0])
            rtext = residence_texts_t.iloc[rint]
        elif resident == False:
            rint = np.random.randint(0, residence_texts_f.shape[0])        
            rtext = residence_texts_f.iloc[rint]
        newtemplate = newtemplate.replace('FACT2', rtext)
    
    # diurnal
    if pd.isna(diurnal):
        newtemplate = newtemplate.replace('<p>FACT3</p>', '')
    else:
        if diurnal == True:
            rint = np.random.randint(0, diurnal_texts_t.shape[0])
            dtext = diurnal_texts_t.iloc[rint]
        elif diurnal == False:
            rint = np.random.randint(0, diurnal_texts_f.shape[0])        
            dtext = diurnal_texts_f.iloc[rint]
        newtemplate = newtemplate.replace('FACT3', dtext)
    
    # abundance
    if pd.isna(abundance):
        newtemplate = newtemplate.replace('<p>FACT4</p>', '')
    else:    
        if abundance == True:
            rint = np.random.randint(0, abundance_texts_t.shape[0])
            atext = abundance_texts_t.iloc[rint]
        elif abundance == False:
            rint = np.random.randint(0, abundance_texts_f.shape[0])        
            atext = abundance_texts_f.iloc[rint]
        newtemplate = newtemplate.replace('FACT4', atext)
    
    # mass
    if pd.isna(mass):
        newtemplate = newtemplate.replace('<p>FACT5</p>', '')
    else:
        if mass == True:
            rint = np.random.randint(0, mass_texts_t.shape[0])
            mtext = mass_texts_t.iloc[rint]
        elif abundance == False:
            rint = np.random.randint(0, mass_texts_f.shape[0])        
            mtext = mass_texts_f.iloc[rint]
        newtemplate = newtemplate.replace('FACT5', mtext)
    
    # pickiness
    if pd.isna(pickiness):
        newtemplate = newtemplate.replace('<p>FACT6</p>', '')
    else:
        if pickiness == 'O':
            rint = np.random.randint(0, pick_texts_o.shape[0])
            ptext = pick_texts_o.iloc[rint]
        elif pickiness == 'P':
            rint = np.random.randint(0, pick_texts_p.shape[0])
            ptext = pick_texts_p.iloc[rint]
        elif pickiness == 'M':
            rint = np.random.randint(0, pick_texts_m.shape[0])
            ptext = pick_texts_m.iloc[rint]
        newtemplate = newtemplate.replace('FACT6', ptext)
    
    # image url
    if pd.isna(imgurl):
        imgurl = "https://placeimg.com/600/300/nature"
    newtemplate = newtemplate.replace('IMAGEURL', imgurl)
    if pd.isna(imgatt):
        imgatt = ''
    newtemplate = newtemplate.replace('IMGATT', '"' + imgatt + '"')
    
    newtemplates.append(newtemplate)

# 6) Write beginning, edited templates and end to new file
# Shuffle order of edited templates to randomise the order of the cards
random.shuffle(newtemplates)
outdir = os.path.dirname(templatefile)
outpath = os.path.join(outdir, 'testindex.html')
with open(outpath, mode='w+', encoding='utf-8') as outfile:
    outfile.writelines(filestart)
    outfile.writelines(newtemplates)
    outfile.writelines(fileend)


