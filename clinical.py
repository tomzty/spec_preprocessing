import xml.etree.ElementTree as ET
import os
import json

folders = os.listdir('clinical_trials.0/')
files = []
for i in folders:
    if 'NCT' in i:
        for j in os.listdir('clinical_trials.0/'+i):
            files.append('clinical_trials.0/'+i+'/'+j)


overallres = dict()
for file in files:
    #print(file)
    root = ET.parse(file).getroot()
    nct_id = root.find('id_info').find('nct_id').text
    brief_title = root.find('brief_title').text
    official_title = root.find('official_title')
    if official_title:
        official_title = official_title.text
    else:
        official_title = ''
    brief_summary = root.find('brief_summary')
    if brief_summary:
        brief_summary = brief_summary.find('textblock').text
        brief_summary = brief_summary.replace('rationale','')
        brief_summary = brief_summary.replace('objective','')
        brief_summary = brief_summary.replace('\n','')
    else:
        brief_summary = ''
    detailed_description = root.find('detailed_description')
    if detailed_description:
        detailed_description = detailed_description.find('textblock').text
        detailed_description = detailed_description.replace('rationale','')
        detailed_description = detailed_description.replace('objective','')
        detailed_description = detailed_description.replace('\n','')
    else:
        detailed_description = ''
    study_type = root.find('study_type').text
    intervention = root.find('intervention')
    if intervention:
        intervention_type = intervention.find('intervention_type').text
    else:
        intervention_type = ''
    eligibility = root.find('eligibility')
    if eligibility:
        criteria = eligibility.find('criteria')
        if criteria:
            criteria = root.find('eligibility').find('criteria').find('textblock').text
            if 'Inclusion Criteria' in criteria and 'Exclusion Criteria' in criteria:
                temp = criteria.split('Inclusion Criteria')[1].split('Exclusion Criteria')
                if len(temp)==2:
                    inclusion_criteria = criteria.split('Inclusion Criteria')[1].split('Exclusion Criteria')[0]
                    exclusion_criteria = criteria.split('Inclusion Criteria')[1].split('Exclusion Criteria')[1]
                    inclusion_criteria = inclusion_criteria.replace('rationale','')
                    inclusion_criteria = inclusion_criteria.replace('objective','')
                    inclusion_criteria = inclusion_criteria.replace('\n','')
                    exclusion_criteria = exclusion_criteria.replace('rationale','')
                    exclusion_criteria = exclusion_criteria.replace('objective','')
                    exclusion_criteria = exclusion_criteria.replace('\n','')
                else:
                    inclusion_criteria = ''
                    exclusion_criteria = ''
            else:
                inclusion_criteria = ''
                exclusion_criteria = ''
        else:
            inclusion_criteria = ''
            exclusion_criteria = ''
        
        healthy_volunteers = root.find('eligibility').find('healthy_volunteers')
        if healthy_volunteers:
            healthy_volunteers = healthy_volunteers.text
        else:
            healthy_volunteers = ''
    else:
        inclusion_criteria = ''
        exclusion_criteria = ''
        healthy_volunteers = ''
    keywordlist = []
    keywords = root.findall('keyword')
    for i in keywords:
        keywordlist.append(i.text)
    condition_browse = root.find('condition_browse')
    if condition_browse:
        meshterms = condition_browse.findall('mesh_term')
    else:
        meshterms = []
    mesh_term_list = []
    for i in meshterms:
        mesh_term_list.append(i.text)
    res = dict()
    #res['nct_id'] = nct_id
    res['brief_title'] = brief_title
    res['official_title'] = official_title
    res['brief_summary'] = brief_summary
    res['detailed_description'] = detailed_description
    res['study_type'] = study_type
    res['intervention_type'] = intervention_type
    res['inclusion_criteria'] = inclusion_criteria
    res['exclusion_criteria'] = exclusion_criteria
    res['healthy_volunteers'] = healthy_volunteers
    res['keyword'] = keywordlist
    res['meshterm'] = mesh_term_list
    overallres[nct_id]=res

with open('output_test_clinical_temp.json','w') as output:
    json.dump(overallres,output,indent = 4)