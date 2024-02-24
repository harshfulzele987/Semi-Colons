from flask import *
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import json 
from flask_login import LoginManager
app = Flask(__name__)

@app.route('/BuSummaryMediaAndDev', methods=['GET', 'POST'])
def index():
    if request.method=="GET":
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'

        Projection = ['csp','nw_oem_cisco','bu summary telecom','media and ent','silicon and devices','uc and collab','bu summary media&dev','telecom and media']

        Opportunity_projection_23_24 = pd.read_excel(file, sheet_name=1,skiprows=[0])
        Revenue_projection_23_24 = pd.read_excel(file, sheet_name=2,skiprows=[0])
        Revenue_projection_24_25 = pd.read_excel(file, sheet_name=3,skiprows=[0])
        Opportunity_projection_24_25 = pd.read_excel(file, sheet_name=4,skiprows=[0])

        opp = Opportunity_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        opp25 = Opportunity_projection_24_25.select_dtypes(include=np.number).columns.tolist()

        rev = Revenue_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        rev25 = Revenue_projection_24_25.select_dtypes(include=np.number).columns.tolist()

        Opportunity_projection_23_24 = Opportunity_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_23_24 = Revenue_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_24_25 = Revenue_projection_24_25.apply(lambda x: x.astype(str).str.lower())
        Opportunity_projection_24_25 = Opportunity_projection_24_25.apply(lambda x: x.astype(str).str.lower())


        Revenue_projection_23_24[rev] = Revenue_projection_23_24[rev].apply(pd.to_numeric, errors='coerce', axis=1)
        
        Revenue_projection_24_25[rev25] = Revenue_projection_24_25[rev25].apply(pd.to_numeric, errors='coerce', axis=1)

        Opportunity_projection_23_24[opp] = Opportunity_projection_23_24[opp].apply(pd.to_numeric, errors='coerce', axis=1)


        Opportunity_projection_24_25[opp25] = Opportunity_projection_24_25[opp25].apply(pd.to_numeric, errors='coerce', axis=1)


        Q4 = []
        for i in range(3,6):
            print(i)
            ab = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Final Revenue'].sum() / 1000.0
            Q4.append(ab)  


        DP = []
        for i in range(3,6):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'yes']['Q4 DP View'].sum() / 1000
            DP.append(ab)


        DP_Non = []
        for i in range(3,6):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'no']['Q4 DP View'].sum() / 1000
            DP_Non.append(ab)    

        Q4FY24 = [sum(x) for x in zip(Q4,DP,DP_Non)]

        a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[5]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']]

        R_uncertain = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum() / 1000
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()

            
            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            R_uncertain.append(ab6)

        
        Op_tbcr = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'opp to be created']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'opp to be createdy']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Op_tbcr.append(ab6)

        Staff_depen = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Staff_depen.append(ab6)

        New_oppo = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            New_oppo.append(ab6)


        Proactive = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Proactive.append(ab6)

        RFP = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            RFP.append(ab6)

        Gov = []
        for i in range(3,6):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Gov.append(ab6)

        print('Gov--->',Gov)


        print("------------------------------------")
        print(R_uncertain,Op_tbcr,Staff_depen,New_oppo,Proactive,RFP,Gov)
        Q4FY24_Bridge_Total = [sum(x) for x in zip(R_uncertain,Op_tbcr,Staff_depen,New_oppo,Proactive,RFP,Gov)]

        
        Low_confi_bridge = []
        for i in range(3,6):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Low_confi_bridge.append(ab)

        Med_confi_bridge = []
        for i in range(3,6):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Med_confi_bridge.append(ab)

        High_confi_bridge = []
        for i in range(3,6):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            ab = (a+b) / 1000
            High_confi_bridge.append(ab)

        FY24_Forecast = [sum(x) for x in zip(High_confi_bridge,Q4FY24)]
        
        Tw_LW_Difference = [-541, -570,-2438]

        BU_QR_RTS_pending = sum(Q4)

        DP_view = sum(DP)

        DP_view_non = sum(DP_Non)

        Q1FY24 = BU_QR_RTS_pending+DP_view+DP_view_non

        renewal_uncertainity = sum(R_uncertain)
        Op = sum(Op_tbcr)
        Staffing_dependent = sum(Staff_depen)
        New_opportunities = sum(New_oppo)
        Proactive_pitch = sum(Proactive)
        rfp = sum(RFP)
        Others = sum(Gov)

        Q1FY24BridgeTotal = renewal_uncertainity+Op+Staffing_dependent+New_opportunities+Proactive_pitch+rfp+Others

        TBC_Opportunity = 0

        Low_confidence_Bridge = sum(Low_confi_bridge)
        Medium_confidence_Bridge = sum(Med_confi_bridge)
        High_confidence_Bridge = sum(High_confi_bridge)

        FY25Forecast = Q1FY24+Low_confidence_Bridge+TBC_Opportunity+High_confidence_Bridge

        BU_TW_LW_Difference = -3550

        print(Q4FY24_Bridge_Total)

        Dict = {'BU':"MEDIA&DEVICES","Data":{
'Date':["12-Feb-23","19-Feb-23"],
'Q4 Vertical Target': [7663, 7663],
'Q1 RTS + Pending':[3791, BU_QR_RTS_pending],
'DP View (CR Oppt)': [60, DP_view],
'DP View (Non-CR Oppt)': [0, DP_view_non],
'Q1FY24': [3851, Q1FY24],
'Renewal uncertainty': [0, renewal_uncertainity], 
    'Opp to be created': [0, Op], 
    'Staffing Dependent': [93, Staffing_dependent], 
    'New opportunities': [2559, New_opportunities],
    'Proactive pitch': [0, Proactive_pitch], 
    'RFP':[0,rfp],
    'Others':[50,Others], 
    'Q1FY24-Bridge Total':[2702,Q1FY24BridgeTotal], 
    'TBC Opportuity':[0,TBC_Opportunity], 
    'Low Confidence Bridge':[1800, Low_confidence_Bridge], 
    'Medium Confidence Bridge':[50, Medium_confidence_Bridge],
    'High Confidence Bridge':[852, High_confidence_Bridge], 
    'FY24 Forecast (incl High Confidence Bridge)':[4703, FY25Forecast], 
    'TW-LW Difference':[-3550]},
    "DU":{
        "UC and Collab":{
            'Date':["12-Feb-23","19-Feb-23"],
            'Q4 Vertical Target': [3656, 3656],
            'Q1 RTS + Pending':[2523, Q4[2]],
            'DP View (CR Oppt)': [43, DP[2]],
            'DP View (Non-CR Oppt)': [0, DP_Non[2]],
            'Q4FY24': [2566, Q4FY24[2]],
            'Renewal uncertainty': [0, R_uncertain[2]], 
                'Opp to be created': [0, Op_tbcr[2]], 
                'Staffing Dependent': [0, Staff_depen[2]], 
                'New opportunities': [50, New_oppo[2]],
                'Proactive pitch': [0, Proactive], 
                'RFP':[0,RFP],
                'Others':[0,Gov], 
                'Q1FY24-Bridge Total':[50,Q4FY24_Bridge_Total[0]], #Edited .................
                'TBC Opportuity':[0,TBC_Opportunity], 
                'Low Confidence Bridge':[0, Low_confi_bridge[2]], 
                'Medium Confidence Bridge':[50, Med_confi_bridge[2]],
                'High Confidence Bridge':[0, High_confi_bridge[2]], 
                'FY24 Forecast (incl High Confidence Bridge)':[2566, FY24_Forecast[2]], 
                'TW-LW Difference':[-2438]
        },
        "Silicon and Devices": {
            "Data":{
            'Date':["12-Feb-23","19-Feb-23"],
            'Q4 Vertical Target': [1263, 1263],
            'Q1 RTS + Pending':[317, Q4[1]],
            'DP View (CR Oppt)': [17, DP[1]],
            'DP View (Non-CR Oppt)': [0, DP_Non[1]],
            'Q4FY24': [334, Q4FY24[1]],
            'Renewal uncertainty': [0, R_uncertain[1]], 
                'Opp to be created': [0, Op_tbcr[1]], 
                'Staffing Dependent': [48, Staff_depen[1]], 
                'New opportunities': [709, New_oppo[1]],
                'Proactive pitch': [0, Proactive], 
                'RFP':[0,RFP],
                'Others':[50,Gov], 
                'Q1FY24-Bridge Total':[807,Q4FY24_Bridge_Total[1]], 
                'TBC Opportuity':[0,TBC_Opportunity], 
                'Low Confidence Bridge':[0, Low_confi_bridge[1]], 
                'Medium Confidence Bridge':[0, Med_confi_bridge[1]],
                'High Confidence Bridge':[807, High_confi_bridge[1]], 
                'FY24 Forecast (incl High Confidence Bridge)':[1141, FY24_Forecast[1]], 
                'TW-LW Difference':[-570],
            },
        },
        "Media and Ent": {
            "Data":{
            'Date':["12-Feb-23","19-Feb-23"],
            'Q4 Vertical Target': [1389, 1389],
            'Q1 RTS + Pending':[951, Q4[0]],
            'DP View (CR Oppt)': [0, DP[0]],
            'DP View (Non-CR Oppt)': [0, DP_Non[0]],
            'Q4FY24': [951, Q4FY24[0]],
            'Renewal uncertainty': [0, R_uncertain[0]], 
                'Opp to be created': [0, Op_tbcr[0]], 
                'Staffing Dependent': [45, Staff_depen[0]], 
                'New opportunities': [1800, New_oppo[0]],
                'Proactive pitch': [0, Proactive], 
                'RFP':[0,RFP],
                'Others':[50,Gov], 
                'Q1FY24-Bridge Total':[1845,Q4FY24_Bridge_Total[0]], 
                'TBC Opportuity':[0,TBC_Opportunity], 
                'Low Confidence Bridge':[1800, Low_confi_bridge[0]], 
                'Medium Confidence Bridge':[0, Med_confi_bridge[0]],
                'High Confidence Bridge':[45, High_confi_bridge[0]], 
                'FY24 Forecast (incl High Confidence Bridge)':[996, FY24_Forecast[0]], 
                'TW-LW Difference':[-541],
            },
            
        },
    }

}
    return Dict

@app.route('/Opportunity_projection_24_25', methods=['GET', 'POST'])
def Opportunity_24_25():
    if request.method == "GET":
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'
        Opportunity_projection_24_25 = pd.read_excel(file, sheet_name=4,skiprows=[0])
        Opportunity_projection_24_25_json = Opportunity_projection_24_25.to_json()
    return Opportunity_projection_24_25_json

@app.route('/Revenue_projection_24_25', methods=['GET', 'POST'])
def Revenue_24_25():
    if request.method == "GET":
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'  
        Revenue_projection_24_25 = pd.read_excel(file, sheet_name=3,skiprows=[0])
        Revenue_projection_24_25_json = Revenue_projection_24_25.to_json()
    return Revenue_projection_24_25_json

@app.route('/Opportunity_projection_23_24', methods=['GET', 'POST'])
def Opportunity_23_24():
    if request.method == "GET":
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'
        Opportunity_projection_23_24 = pd.read_excel(file, sheet_name=4,skiprows=[0])
        Opportunity_projection_23_24_json = Opportunity_projection_23_24.to_json()
    return Opportunity_projection_23_24_json

@app.route('/Revenue_projection_23_24', methods=['GET', 'POST'])
def Revenue_23_24():
    if request.method == "GET":
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'  
        Revenue_projection_23_24 = pd.read_excel(file, sheet_name=3,skiprows=[0])
        Revenue_projection_23_24_json = Revenue_projection_23_24.to_json()
    return Revenue_projection_23_24_json

@app.route('/BuSummaryTelecom' , methods=['GET' , 'POST'])
def BuSummaryMediaAndDev():
    if request.method == 'GET':
        file = "C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx"
        Projection = ['csp','nw_oem_cisco','bu summary telecom','media and ent','silicon and devices','uc and collab','bu summary media&dev','telecom and media']
        
        Opportunity_projection_23_24 = pd.read_excel(file, sheet_name=1,skiprows=[0])
        Revenue_projection_23_24 = pd.read_excel(file, sheet_name=2,skiprows=[0])
        Revenue_projection_24_25 = pd.read_excel(file, sheet_name=3,skiprows=[0])
        Opportunity_projection_24_25 = pd.read_excel(file, sheet_name=4,skiprows=[0])

        opp = Opportunity_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        opp25 = Opportunity_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        
        rev = Revenue_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        rev25 = Revenue_projection_24_25.select_dtypes(include=np.number).columns.tolist()
        
        Opportunity_projection_23_24 = Opportunity_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_23_24 = Revenue_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_24_25 = Revenue_projection_24_25.apply(lambda x: x.astype(str).str.lower())
        Opportunity_projection_24_25 = Opportunity_projection_24_25.apply(lambda x: x.astype(str).str.lower())
        
        Revenue_projection_23_24[rev] = Revenue_projection_23_24[rev].apply(pd.to_numeric, errors='coerce', axis=1)
        Revenue_projection_24_25[rev25] = Revenue_projection_24_25[rev25].apply(pd.to_numeric, errors='coerce', axis=1)
        Opportunity_projection_23_24[opp] = Opportunity_projection_23_24[opp].apply(pd.to_numeric, errors='coerce', axis=1)
        Opportunity_projection_24_25[opp25] = Opportunity_projection_24_25[opp25].apply(pd.to_numeric, errors='coerce', axis=1)
        Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[0]]['Q4 Final Revenue'].sum() / 1000.0
        Q4 = []
        for i in range(0,2):
            print(i)
            ab = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Final Revenue'].sum() / 1000.0
            Q4.append(ab)
        DP = []
        for i in range(0,2):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'yes']['Q4 DP View'].sum() / 1000
            DP.append(ab)
        DP_Non = []
        for i in range(0,2):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'no']['Q4 DP View'].sum() / 1000
            DP_Non.append(ab)
        Q4FY24 = [sum(x) for x in zip(Q4,DP,DP_Non)]
        
        a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[5]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']]
        
        R_uncertain = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum() / 1000
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()

            
            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            R_uncertain.append(ab6)

        Op_tbcr = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'opp to be created']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'opp to be createdy']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Op_tbcr.append(ab6)
        Staff_depen = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Staff_depen.append(ab6)    
        New_oppo = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            New_oppo.append(ab6)
            
        Proactive = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Proactive.append(ab6)
            
        RFP = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            RFP.append(ab6)
            
        Gov = []
        for i in range(0,2):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Gov.append(ab6)
        Q4FY24_Bridge_Total = [sum(x) for x in zip(R_uncertain,Op_tbcr,Staff_depen,New_oppo,Proactive,RFP,Gov)]
        Low_confi_bridge = []
        for i in range(0,2):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Low_confi_bridge.append(ab)
        Med_confi_bridge = []
        for i in range(0,2):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Med_confi_bridge.append(ab)
        High_confi_bridge = []
        for i in range(0,2):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            ab = (a+b) / 1000
            High_confi_bridge.append(ab)
        FY24_Forecast = [sum(x) for x in zip(High_confi_bridge,Q4FY24)]
        Tw_LW_Difference = [-541, -570,-2438]
        BU_QR_RTS_pending = sum(Q4)
        DP_view = sum(DP)
        DP_view_non = sum(DP_Non)
        Q1FY24 = BU_QR_RTS_pending+DP_view+DP_view_non
        renewal_uncertainity = sum(R_uncertain)
        Op = sum(Op_tbcr)
        Staffing_dependent = sum(Staff_depen)
        New_opportunities = sum(New_oppo)
        Proactive_pitch = sum(Proactive)
        rfp = sum(RFP)
        Others = sum(Gov)
        Q1FY24BridgeTotal = renewal_uncertainity+Op+Staffing_dependent+New_opportunities+Proactive_pitch+rfp+Others
        TBC_Opportunity = 0
        Low_confidence_Bridge = sum(Low_confi_bridge)
        Medium_confidence_Bridge = sum(Med_confi_bridge)
        High_confidence_Bridge = sum(High_confi_bridge)
        FY25Forecast = Q1FY24+Low_confidence_Bridge+TBC_Opportunity+High_confidence_Bridge
        BU_TW_LW_Difference = -3210
        Dict = {'BU':"TELECOM","Data":{
    'Date':["12-Feb-23","19-Feb-23"],
    'Q4 Vertical Target': [9730, 9730],
    'Q1 RTS + Pending':[5089, BU_QR_RTS_pending],
    'DP View (CR Oppt)': [523, DP_view],
    'DP View (Non-CR Oppt)': [306, DP_view_non],
    'Q1FY24': [5918, Q1FY24],
    'Renewal uncertainty': [0, renewal_uncertainity], 
     'Opp to be created': [174, Op], 
     'Staffing Dependent': [54, Staffing_dependent], 
     'New opportunities': [3705, New_opportunities],
     'Proactive pitch': [0, Proactive_pitch], 
     'RFP':[0,rfp],
     'Others':[0,Others], 
     'Q1FY24-Bridge Total':[3933,Q1FY24BridgeTotal], 
     'TBC Opportuity':[0,TBC_Opportunity], 
     'Low Confidence Bridge':[110, Low_confidence_Bridge], 
     'Medium Confidence Bridge':[204, Medium_confidence_Bridge],
     'High Confidence Bridge':[3619, High_confidence_Bridge], 
     'FY24 Forecast (incl High Confidence Bridge)':[9537, FY25Forecast], 
     'TW-LW Difference':[-3210]},
       "DU":{
           "NW_OEM_Cisco": {
                "Data":{
                'Date':["12-Feb-23","19-Feb-23"],
                'Q4 Vertical Target': [6032, 6032],
                'Q1 RTS + Pending':[3001, Q4[1]],
                'DP View (CR Oppt)': [344, DP[1]],
                'DP View (Non-CR Oppt)': [306, DP_Non[1]],
                'Q4FY24': [3651, Q4FY24[1]],
                'Renewal uncertainty': [0, R_uncertain[1]], 
                 'Opp to be created': [30, Op_tbcr[1]], 
                 'Staffing Dependent': [0, Staff_depen[1]], 
                 'New opportunities': [2632, New_oppo[1]],
                 'Proactive pitch': [0, Proactive], 
                 'RFP':[0,RFP],
                 'Others':[0,Gov], 
                 'Q1FY24-Bridge Total':[2662,Q4FY24_Bridge_Total[1]], 
                 'TBC Opportuity':[0,TBC_Opportunity], 
                 'Low Confidence Bridge':[0, Low_confi_bridge[1]], 
                 'Medium Confidence Bridge':[51, Med_confi_bridge[1]],
                 'High Confidence Bridge':[2611, High_confi_bridge[1]], 
                 'FY24 Forecast (incl High Confidence Bridge)':[6262, FY24_Forecast[1]], 
                 'TW-LW Difference':[0],
                },
           },
           "CSP": {
                "Data":{
                'Date':["12-Feb-23","19-Feb-23"],
                'Q4 Vertical Target': [3758, 3758],
                'Q1 RTS + Pending':[2089, Q4[0]],
                'DP View (CR Oppt)': [179, DP[0]],
                'DP View (Non-CR Oppt)': [0, DP_Non[0]],
                'Q4FY24': [2268, Q4FY24[0]],
                'Renewal uncertainty': [0, R_uncertain[0]], 
                 'Opp to be created': [144, Op_tbcr[0]], 
                 'Staffing Dependent': [54, Staff_depen[0]], 
                 'New opportunities': [1073, New_oppo[0]],
                 'Proactive pitch': [0, Proactive], 
                 'RFP':[0,RFP],
                 'Others':[0,Gov], 
                 'Q1FY24-Bridge Total':[1271,Q4FY24_Bridge_Total[0]], 
                 'TBC Opportuity':[0,TBC_Opportunity], 
                 'Low Confidence Bridge':[110, Low_confi_bridge[0]], 
                 'Medium Confidence Bridge':[153, Med_confi_bridge[0]],
                 'High Confidence Bridge':[1008, High_confi_bridge[0]], 
                 'FY24 Forecast (incl High Confidence Bridge)':[3276, FY24_Forecast[0]], 
                 'TW-LW Difference':[-3210],
                },
               
           },
       }
    
    }
        return Dict
        
@app.route('/OuTeleconAndMedia' , methods=['GET' , 'POST'])
def OuTeleconAndMedia():
    if request.method == 'GET':
        file  = 'C:/Users/Harsh_Fulzele/Documents/Semi-Colons/Dashboard_Summary_Sample.xlsx'
        Projection = ['csp','nw_oem_cisco','media and ent','silicon and devices','uc and collab','telecom and media']
        Opportunity_projection_23_24 = pd.read_excel(file, sheet_name=1,skiprows=[0])
        Revenue_projection_23_24 = pd.read_excel(file, sheet_name=2,skiprows=[0])
        Revenue_projection_24_25 = pd.read_excel(file, sheet_name=3,skiprows=[0])
        Opportunity_projection_24_25 = pd.read_excel(file, sheet_name=4,skiprows=[0])
        
        opp = Opportunity_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        opp25 = Opportunity_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        rev = Revenue_projection_23_24.select_dtypes(include=np.number).columns.tolist()
        rev25 = Revenue_projection_24_25.select_dtypes(include=np.number).columns.tolist()  
        
        Opportunity_projection_23_24 = Opportunity_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_23_24 = Revenue_projection_23_24.apply(lambda x: x.astype(str).str.lower())
        Revenue_projection_24_25 = Revenue_projection_24_25.apply(lambda x: x.astype(str).str.lower())
        Opportunity_projection_24_25 = Opportunity_projection_24_25.apply(lambda x: x.astype(str).str.lower())
        
        Revenue_projection_23_24[rev] = Revenue_projection_23_24[rev].apply(pd.to_numeric, errors='coerce', axis=1)
        Revenue_projection_24_25[rev25] = Revenue_projection_24_25[rev25].apply(pd.to_numeric, errors='coerce', axis=1)
        Opportunity_projection_23_24[opp] = Opportunity_projection_23_24[opp].apply(pd.to_numeric, errors='coerce', axis=1)
        Opportunity_projection_24_25[opp25] = Opportunity_projection_24_25[opp25].apply(pd.to_numeric, errors='coerce', axis=1)
        Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[0]]['Q4 Final Revenue'].sum() / 1000.0
        
        Q4 = []
        for i in range(0,5):
            print(i)
            ab = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Final Revenue'].sum() / 1000.0
            Q4.append(ab)
        
        DP = []
        for i in range(0,5):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'yes']['Q4 DP View'].sum() / 1000
            DP.append(ab)
        
        DP_Non = []
        for i in range(0,5):
            print(i)
            a = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Is CR','Q4 DP View']]
            ab = a[a['Is CR'] == 'no']['Q4 DP View'].sum() / 1000
            DP_Non.append(ab)
            
        Q4FY24 = [sum(x) for x in zip(Q4,DP,DP_Non)]
        
        a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[5]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']]
        
        a[a['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum() / 1000
        
        R_uncertain = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum() / 1000
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rewewal uncertainity']['Q4 High Bridge Revenue'].sum()

            
            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rewewal uncertainity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rewewal uncertainity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            R_uncertain.append(ab6)
         
        Op_tbcr = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'opp to be created']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'opp to be createdy']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'opp to be created']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'opp to be created']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Op_tbcr.append(ab6)
        
        Staff_depen = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()
            
            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'staffing dependent']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'staffing dependent']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'staffing dependent']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Staff_depen.append(ab6)
        New_oppo = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'new opportunity']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'new opportunity']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'new opportunity']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            New_oppo.append(ab6)
        Proactive = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'proactive pitch']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'proactive pitch']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'proactive pitch']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Proactive.append(ab6)
        RFP = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'rfp']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'rfp']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'rfp']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            RFP.append(ab6)
        Gov = []
        for i in range(0,5):
            print(i)
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab = a[a['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a1 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab1 = a1[a1['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()
            
            a2 = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab2 = a2[a2['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            a3 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 High Bridge Revenue','Q4 High Bridge Category']] 
            ab3 = a3[a3['Q4 High Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 High Bridge Revenue'].sum()

            a4 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Medium Bridge Revenue','Q4 Medium Bridge Category']] 
            ab4 = a4[a4['Q4 Medium Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Medium Bridge Revenue'].sum()

            a5 = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]][['Q4 Low Bridge Revenue','Q4 Low Bridge Category']] 
            ab5 = a5[a5['Q4 Low Bridge Category'] == 'others(govt/unplanned leaves/buffers etc.)']['Q4 Low Bridge Revenue'].sum()
            
            ab6 = (ab+ab1+ab2+ab3+ab4+ab5) / 1000
            Gov.append(ab6)
        Q4FY24_Bridge_Total = [sum(x) for x in zip(R_uncertain,Op_tbcr,Staff_depen,New_oppo,Proactive,RFP,Gov)]
        
        Low_confi_bridge = []
        for i in range(0,5):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Low Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Low_confi_bridge.append(ab)
            
        Med_confi_bridge = []
        for i in range(0,5):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 Medium Bridge Revenue'].sum()
            ab = (a+b) / 1000
            Med_confi_bridge.append(ab)
            
        High_confi_bridge = []
        for i in range(0,5):
            a = Revenue_projection_23_24[Revenue_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            b = Opportunity_projection_23_24[Opportunity_projection_23_24['DU Name'] == Projection[i]]['Q4 High Bridge Revenue'].sum()
            ab = (a+b) / 1000
            High_confi_bridge.append(ab)
        FY24_Forecast = [sum(x) for x in zip(High_confi_bridge,Q4FY24)]
        Tw_LW_Difference = [-541, -570,-2438]
        BU_QR_RTS_pending = sum(Q4)
        DP_view = sum(DP)
        DP_view_non = sum(DP_Non)
        Q1FY24 = BU_QR_RTS_pending+DP_view+DP_view_non
        renewal_uncertainity = sum(R_uncertain)
        Op = sum(Op_tbcr)
        Staffing_dependent = sum(Staff_depen)
        New_opportunities = sum(New_oppo)
        Proactive_pitch = sum(Proactive)
        rfp = sum(RFP)
        Others = sum(Gov)
        
        Q1FY24BridgeTotal = renewal_uncertainity+Op+Staffing_dependent+New_opportunities+Proactive_pitch+rfp+Others
        TBC_Opportunity = 0
        Low_confidence_Bridge = sum(Low_confi_bridge)
        Medium_confidence_Bridge = sum(Med_confi_bridge)
        High_confidence_Bridge = sum(High_confi_bridge)
        
        FY25Forecast = Q1FY24+Low_confidence_Bridge+TBC_Opportunity+High_confidence_Bridge
        OU_TW_LW_Difference = -6760
        Dict = {'OU':"TELECOM AND MEDIA","Data":{
    'Date':["12-Feb-23","19-Feb-23"],
    'Q4 Vertical Target': [17393, 17393],
    'Q1 RTS + Pending':[8880, BU_QR_RTS_pending],
    'DP View (CR Oppt)': [583, DP_view],
    'DP View (Non-CR Oppt)': [306, DP_view_non],
    'Q1FY24': [9769, Q1FY24],
    'Renewal uncertainty': [0, renewal_uncertainity], 
     'Opp to be created': [174, Op], 
     'Staffing Dependent': [147, Staffing_dependent], 
     'New opportunities': [6264, New_opportunities],
     'Proactive pitch': [0, Proactive_pitch], 
     'RFP':[0,rfp],
     'Others':[50,Others], 
     'Q1FY24-Bridge Total':[6635,Q1FY24BridgeTotal], 
     'TBC Opportuity':[0,TBC_Opportunity], 
     'Low Confidence Bridge':[1910, Low_confidence_Bridge], 
     'Medium Confidence Bridge':[254, Medium_confidence_Bridge],
     'High Confidence Bridge':[4471, High_confidence_Bridge], 
     'FY24 Forecast (incl High Confidence Bridge)':[14240, FY25Forecast], 
     'TW-LW Difference':[-6760]},
    }
        return Dict
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
                 
if __name__ == "__main__":
    app.run(debug= True)



