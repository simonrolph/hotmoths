import os
import random
import pandas as pd
import numpy as np

# we want to generate the html for the website from the template
# and the database that we will have created in data/stats_for_page.csv
# and data/text_from_facts.csv 

templatefile = '../indextemplate.html'
outputfile = '../index.html'
statsfile = '../../data/cleaned_stats_for_page.csv'
textfile = '../../data/text_from_facts2.csv'
tstartline = 61 # <div class="tinder-cards" id="tindercards"> line
tendline   = 86 # </div> of last moth tinder card line (not the bottom card)

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
      width="600"
      height="300"
      title=IMGATT/>
      <h3>MOTHNAME</h3>
      <span class="sci-name">SCINAME</span>
      <p><a id="locationtext"><i class="fa fa-map-marker"></i> <span class="moth-dist-1">?</span> km from your location</a></p>
'''
ptemplate = 'FACT'
templateend = '    </div>'
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
    
    ptemplates = []
    
    # 5) Edit template with data from step 4
    newtemplate = template.replace('MOTHNAME', mothname)
    newtemplate = newtemplate.replace('SCINAME', sciname)
    
    if pd.isna(plants):
        pass
    else:
        newptemplate = ptemplate.replace('FACT', 'Fave plants: ' + str(plants))
        ptemplates.append(newptemplate)
    
    # resident
    if pd.isna(resident):
        pass
    else:
        if resident == True:
            rint = np.random.randint(0, residence_texts_t.shape[0])
            rtext = residence_texts_t.iloc[rint]
        elif resident == False:
            rint = np.random.randint(0, residence_texts_f.shape[0])        
            rtext = residence_texts_f.iloc[rint]
        newptemplate = ptemplate.replace('FACT', rtext)
        ptemplates.append(newptemplate)
    
    # diurnal
    if pd.isna(diurnal):
        pass
    else:
        if diurnal == True:
            rint = np.random.randint(0, diurnal_texts_t.shape[0])
            dtext = diurnal_texts_t.iloc[rint]
        elif diurnal == False:
            rint = np.random.randint(0, diurnal_texts_f.shape[0])        
            dtext = diurnal_texts_f.iloc[rint]
        newptemplate = ptemplate.replace('FACT', dtext)
        ptemplates.append(newptemplate)
    
    # abundance
    if pd.isna(abundance):
        pass
    else:    
        if abundance == True:
            rint = np.random.randint(0, abundance_texts_t.shape[0])
            atext = abundance_texts_t.iloc[rint]
        elif abundance == False:
            rint = np.random.randint(0, abundance_texts_f.shape[0])        
            atext = abundance_texts_f.iloc[rint]
        newptemplate = ptemplate.replace('FACT', atext)
        ptemplates.append(newptemplate)
    
    # mass
    if pd.isna(mass):
        pass
    else:
        if mass == True:
            rint = np.random.randint(0, mass_texts_t.shape[0])
            mtext = mass_texts_t.iloc[rint]
        elif abundance == False:
            rint = np.random.randint(0, mass_texts_f.shape[0])        
            mtext = mass_texts_f.iloc[rint]
        newptemplate = ptemplate.replace('FACT', mtext)
        ptemplates.append(newptemplate)
    
    # pickiness
    if pd.isna(pickiness):
        pass
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
        newptemplate = ptemplate.replace('FACT', ptext)
        ptemplates.append(newptemplate)
    
    # image url
    if pd.isna(imgurl):
        imgurl = "images/no-image.png"
    newtemplate = newtemplate.replace('IMAGEURL', imgurl)
    if pd.isna(imgatt):
        imgatt = ''
    newtemplate = newtemplate.replace('IMGATT', '"' + imgatt + '"')
    
    random.shuffle(ptemplates)
    
    # randomly group some into paragraphs
    if len(ptemplates) == 1:
        newptemplates = ['<p>' + ptemplates[0] + '</p>']
    elif len(ptemplates) == 0:
        pass
    else:
        newptemplates = []
        for t in range(0, len(ptemplates)):
            rint = np.random.randint(0, 2)
            if t == 0:
                if rint == 0:
                    if ptemplates[t][-1] == '.':
                        newptemplate2 = ptemplates[t] + ' '
                    else:
                        newptemplate2 = ptemplates[t] + '. '
                elif rint == 1:
                    newptemplate2 = ptemplates[t] + '</p>\n<p>'
                newptemplate2 = '<p>' + newptemplate2
            elif t == len(ptemplates)-1:
                newptemplate2 = ptemplates[t] + '</p>'
            else:
                if rint == 0:
                    if ptemplates[t][-1] == '.':
                        newptemplate2 = ptemplates[t] + ' '
                    else:
                        newptemplate2 = ptemplates[t] + '. '
                elif rint == 1:
                    newptemplate2 = ptemplates[t] + '</p>\n<p>'
            newptemplates.append(newptemplate2)
    
    
    ptemplates = ''.join(newptemplates)
    finaltemplate = '\n'.join([newtemplate, ptemplates, templateend])
    newtemplates.append(finaltemplate)

# 6) Write beginning, edited templates and end to new file
# Shuffle order of edited templates to randomise the order of the cards
random.shuffle(newtemplates)
with open(outputfile, mode='w+', encoding='utf-8') as outfile:
    outfile.writelines(filestart)
    outfile.writelines(newtemplates)
    outfile.writelines(fileend)


