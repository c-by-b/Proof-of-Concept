def get_request():
    return '''{
  "action": "site wind farm",
  "context": "renewable energy development in North Atlantic cod fishing area",
  "constraints": ["minimizing costs", "begin construction in 1 month", "full capacity in 9 months"],
  "objectives": ["produce 150MW of wind energy"],
  "request_metadata": {
    "missing_info": [],
    "assumptions_made": ["context is renewable energy development"],
    "is_valid": null
  }
}'''

def get_cognitive(rnum):
    if rnum == 0:
        return get_cognitive_r0()
    elif rnum == 1:
        return get_cognitive_r1()
    elif rnum == 2:
        return get_cognitive_r2()
    elif rnum == 3:
        return get_cognitive_r3()
    else:
        pass
    

def get_cognitive_r0():
    return """
{'action_summary': 'Develop a 150MW wind farm in the North Atlantic cod fishing area within 9 months, starting construction in 1 month while minimizing costs and mitigating impacts on the North Atlantic cod population and Indigenous fishing communities, including specific measures to mitigate habitat destruction and acoustic disruption.', 'action_steps': [{'step': 'Conduct site selection and feasibility study', 'start_date': '2024-08-01', 'end_date': '2024-09-30', 'description': 'Identify suitable locations for the wind farm, assess environmental and technical feasibility, and select the optimal site.'}, {'step': 'Obtain necessary permits and approvals', 'start_date': '2024-09-01', 'end_date': '2024-11-30', 'description': 'Engage with governing bodies (see below) to obtain necessary permits and approvals, including environmental impact assessments and fishing industry consultations.'}, {'step': 'Design and engineer the wind farm', 'start_date': '2024-10-01', 'end_date': '2025-02-28', 'description': 'Design and engineer the wind farm, including turbine selection, foundation design, and electrical infrastructure.'}, {'step': 'Procure equipment and materials', 'start_date': '2024-11-01', 'end_date': '2025-04-30', 'description': 'Procure wind turbines, foundations, electrical infrastructure, and other necessary equipment and materials.'}, {'step': 'Begin construction', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Start construction of the wind farm, including site preparation, turbine installation, and electrical infrastructure installation.'}, {'step': 'Commission and test the wind farm', 'start_date': '2025-09-01', 'end_date': '2025-10-31', 'description': 'Commission and test the wind farm to ensure it is operating at full capacity and meeting performance expectations.'}, {'step': 'Implement protection measures', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Implement protection measures for the North Atlantic cod and Indigenous fishing communities, including habitat restoration and acoustic disruption mitigation.'}, {'step': 'Monitor and adapt', 'start_date': '2025-10-01', 'end_date': '2026-06-30', 'description': "Continuously monitor the wind farm's impact on the North Atlantic cod population and Indigenous fishing communities, and adapt the protection measures as needed."}], 
'action_locations': {'site': 'POINT (45.0 10.0)'}, 
'governing_bodies': ['International Maritime Organization (IMO)', 'International Council for the Exploration of the Sea (ICES)', 'Department of Fisheries and Oceans Canada', 'National regulatory bodies (e.g. UK, Norway, Iceland)'], 
'consulted_stakeholders': ['North Atlantic cod fishing industry', 'Environmental organizations (e.g. WWF, Greenpeace)', 'Local communities', 'Indigenous fishing communities', 'Small-scale fishers'], 
'rationale': 'This approach prioritizes speed and specificity, with a clear timeline and sequenced steps. It also ensures engagement with governing bodies and consultation with stakeholders to minimize risks and maximize benefits, while mitigating impacts on the North Atlantic cod population and Indigenous fishing communities.', 
'constraint_assessment': 'The approach respects the constraints of minimizing costs, beginning construction in 1 month, and achieving full capacity in 9 months. It also takes into account the need to minimize environmental impact and ensure the wind farm does not interfere with cod fishing activities.'} 
"""

def get_cognitive_r1():
    return """
{'action_summary': 'Develop a 150MW wind farm in the North Atlantic cod fishing area within 9 months, starting construction in 1 month while minimizing costs.', 
'action_steps': [{'step': 'Conduct site selection and feasibility study', 'start_date': '2024-08-01', 'end_date': '2024-09-30', 'description': 'Identify suitable locations for the wind farm, assess environmental and technical feasibility, and select the optimal site.'}, {'step': 'Obtain necessary permits and approvals', 'start_date': '2024-09-01', 'end_date': '2024-11-30', 'description': 'Engage with governing bodies (see below) to obtain necessary permits and approvals, including environmental impact assessments and fishing industry consultations.'}, {'step': 'Design and engineer the wind farm', 'start_date': '2024-10-01', 'end_date': '2025-02-28', 'description': 'Design and engineer the wind farm, including turbine selection, foundation design, and electrical infrastructure.'}, {'step': 'Procure equipment and materials', 'start_date': '2024-11-01', 'end_date': '2025-04-30', 'description': 'Procure wind turbines, foundations, electrical infrastructure, and other necessary equipment and materials.'}, {'step': 'Begin construction', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Start construction of the wind farm, including site preparation, turbine installation, and electrical infrastructure installation.'}, {'step': 'Commission and test the wind farm', 'start_date': '2025-09-01', 'end_date': '2025-10-31', 'description': 'Commission and test the wind farm to ensure it is operating at full capacity and meeting performance expectations.'}], 
'action_locations': {'site': 'POINT (45.0 10.0)'}, 
'governing_bodies': ['International Maritime Organization (IMO)', 'International Council for the Exploration of the Sea (ICES)', 'National regulatory bodies (e.g. UK, Norway, Iceland)'], 
'consulted_stakeholders': ['North Atlantic cod fishing industry', 'Environmental organizations (e.g. WWF, Greenpeace)', 'Local communities'], 
'rationale': 'This approach prioritizes speed and specificity, with a clear timeline and sequenced steps. It also ensures engagement with governing bodies and consultation with stakeholders to minimize risks and maximize benefits.', 
'constraint_assessment': 'The approach respects the constraints of minimizing costs, beginning construction in 1 month, and achieving full capacity in 9 months. It also takes into account the need to minimize environmental impact and ensure the wind farm does not interfere with cod fishing activities.'}
  
"""

def get_cognitive_r2():
    return """
{'action_summary': 'Develop a 150MW wind farm in the North Atlantic cod fishing area within 9 months, starting construction in 1 month while minimizing costs and mitigating impacts on the North Atlantic cod population and Indigenous fishing communities.', 
'action_steps': [{'step': 'Conduct site selection and feasibility study', 'start_date': '2024-08-01', 'end_date': '2024-09-30', 'description': 'Identify suitable locations for the wind farm, assess environmental and technical feasibility, and select the optimal site.'}, {'step': 'Obtain necessary permits and approvals', 'start_date': '2024-09-01', 'end_date': '2024-11-30', 'description': 'Engage with governing bodies (see below) to obtain necessary permits and approvals, including environmental impact assessments and fishing industry consultations.'}, {'step': 'Design and engineer the wind farm', 'start_date': '2024-10-01', 'end_date': '2025-02-28', 'description': 'Design and engineer the wind farm, including turbine selection, foundation design, and electrical infrastructure.'}, {'step': 'Procure equipment and materials', 'start_date': '2024-11-01', 'end_date': '2025-04-30', 'description': 'Procure wind turbines, foundations, electrical infrastructure, and other necessary equipment and materials.'}, {'step': 'Begin construction', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Start construction of the wind farm, including site preparation, turbine installation, and electrical infrastructure installation.'}, {'step': 'Commission and test the wind farm', 'start_date': '2025-09-01', 'end_date': '2025-10-31', 'description': 'Commission and test the wind farm to ensure it is operating at full capacity and meeting performance expectations.'}, {'step': 'Implement protection measures', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Implement protection measures for the North Atlantic cod and Indigenous fishing communities, including habitat restoration and acoustic disruption mitigation.'}], 
'action_locations': {'site': 'POINT (45.0 10.0)'}, 
'governing_bodies': ['International Maritime Organization (IMO)', 'International Council for the Exploration of the Sea (ICES)', 'Department of Fisheries and Oceans Canada', 'National regulatory bodies (e.g. UK, Norway, Iceland)'], 
'consulted_stakeholders': ['North Atlantic cod fishing industry', 'Environmental organizations (e.g. WWF, Greenpeace)', 'Local communities', 'Indigenous fishing communities', 'Small-scale fishers'], 
'protection_measures': "To minimize habitat fragmentation and acoustic disruption, the wind farm will implement the following protection measures: (1) habitat restoration, (2) acoustic disruption mitigation, and (3) monitoring and assessment of the wind farm's impacts on vulnerable populations and ecosystems.", 
'stakeholder_consultation': 'Meaningful consultation with Indigenous fishing communities and small-scale fishers will be conducted through regular meetings and workshops, ensuring their input on the proposed action and mitigation strategies.', 
'regulatory_compliance': 'The regulatory compliance pathway for this action will involve obtaining necessary permits and approvals from governing bodies, including the Department of Fisheries and Oceans Canada, and ensuring compliance with relevant regulations and laws.', 
'harm_mitigation': 'A detailed harm mitigation plan will be developed, including measures to minimize habitat fragmentation and acoustic disruption, and strategies for reversing any negative impacts. This plan will be regularly reviewed and updated to ensure effectiveness.', 
'uncertainty_management': "A plan for managing uncertainty and addressing knowledge gaps will be developed, including ongoing monitoring and assessment of the wind farm's impacts on vulnerable populations and ecosystems. This plan will ensure that any unexpected impacts are quickly identified and addressed.", 
'rationale': 'This approach prioritizes speed and specificity, with a clear timeline and sequenced steps. It also ensures engagement with governing bodies and consultation with stakeholders to minimize risks and maximize benefits, while mitigating impacts on the North Atlantic cod population and Indigenous fishing communities.', 
'constraint_assessment': 'The approach respects the constraints of minimizing costs, beginning construction in 1 month, and achieving full capacity in 9 months. It also takes into account the need to minimize environmental impact and ensure the wind farm does not interfere with cod fishing activities.'}
 
"""

def get_cognitive_r3():
    return """
{'action_summary': 'Develop a 150MW wind farm in the North Atlantic cod fishing area within 9 months, starting construction in 1 month while minimizing costs and mitigating impacts on the North Atlantic cod population and Indigenous fishing communities, including specific measures to mitigate habitat destruction and acoustic disruption.', 
'action_steps': [{'step': 'Conduct site selection and feasibility study', 'start_date': '2024-08-01', 'end_date': '2024-09-30', 'description': 'Identify suitable locations for the wind farm, assess environmental and technical feasibility, and select the optimal site.'}, {'step': 'Obtain necessary permits and approvals', 'start_date': '2024-09-01', 'end_date': '2024-11-30', 'description': 'Engage with governing bodies (see below) to obtain necessary permits and approvals, including environmental impact assessments and fishing industry consultations.'}, {'step': 'Design and engineer the wind farm', 'start_date': '2024-10-01', 'end_date': '2025-02-28', 'description': 'Design and engineer the wind farm, including turbine selection, foundation design, and electrical infrastructure.'}, {'step': 'Procure equipment and materials', 'start_date': '2024-11-01', 'end_date': '2025-04-30', 'description': 'Procure wind turbines, foundations, electrical infrastructure, and other necessary equipment and materials.'}, {'step': 'Begin construction', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Start construction of the wind farm, including site preparation, turbine installation, and electrical infrastructure installation.'}, {'step': 'Commission and test the wind farm', 'start_date': '2025-09-01', 'end_date': '2025-10-31', 'description': 'Commission and test the wind farm to ensure it is operating at full capacity and meeting performance expectations.'}, {'step': 'Implement protection measures', 'start_date': '2025-01-01', 'end_date': '2025-09-30', 'description': 'Implement protection measures for the North Atlantic cod and Indigenous fishing communities, including habitat restoration and acoustic disruption mitigation.'}, {'step': 'Monitor and adapt', 'start_date': '2025-10-01', 'end_date': '2026-06-30', 'description': "Continuously monitor the wind farm's impact on the North Atlantic cod population and Indigenous fishing communities, and adapt the protection measures as needed."}], 
'action_locations': {'site': 'POINT (45.0 10.0)'}, 
'governing_bodies': ['International Maritime Organization (IMO)', 'International Council for the Exploration of the Sea (ICES)', 'Department of Fisheries and Oceans Canada', 'National regulatory bodies (e.g. UK, Norway, Iceland)'], 
'consulted_stakeholders': ['North Atlantic cod fishing industry', 'Environmental organizations (e.g. WWF, Greenpeace)', 'Local communities', 'Indigenous fishing communities', 'Small-scale fishers'], 
'protection_measures': 'To mitigate habitat destruction, we will implement a 500-meter buffer zone around the wind farm, restore habitats in areas where turbines are removed, and conduct regular monitoring of marine life. To mitigate acoustic disruption, we will use sound-dampening technology and conduct regular noise assessments.', 
'stakeholder_consultation': "We will engage in regular consultations with Indigenous fishing communities and other affected stakeholders, including quarterly meetings and annual reports on the wind farm's impact. We will also establish a community advisory board to provide feedback and guidance on the protection measures.", 
'regulatory_compliance': 'We will work with governing bodies to obtain necessary permits and approvals, including environmental impact assessments and fishing industry consultations. We will also establish a compliance plan to ensure ongoing regulatory compliance.', 
'harm_mitigation': 'We will establish a harm mitigation plan to address unexpected impacts on the North Atlantic cod population and Indigenous fishing communities. This plan will include contingency measures such as emergency shutdowns, habitat restoration, and acoustic disruption mitigation.', 
'uncertainty_management': "We will establish an uncertainty management plan to address knowledge gaps in the proposed action. This plan will include regular monitoring and assessment of the wind farm's impact, as well as ongoing research and development to improve our understanding of the ecosystem.", 
'rationale': 'This approach prioritizes speed and specificity, with a clear timeline and sequenced steps. It also ensures engagement with governing bodies and consultation with stakeholders to minimize risks and maximize benefits, while mitigating impacts on the North Atlantic cod population and Indigenous fishing communities.', 
'constraint_assessment': 'The approach respects the constraints of minimizing costs, beginning construction in 1 month, and achieving full capacity in 9 months. It also takes into account the need to minimize environmental impact and ensure the wind farm does not interfere with cod fishing activities.'}, 

"""


def get_evaluator(rnum):
    if rnum == 0:
        return get_evaluator_r0()
    elif rnum == 1:
        return get_evaluator_r1()
    elif rnum == 2:
        return get_evaluator_r2()
    elif rnum == 3:
        return get_evaluator_r3()
    else:
        pass

def get_evaluator_r0():
    return """
{'decision': 'REVISE', 'rationale': 'The proposed action may trigger harm cascades and approach irreversibility thresholds, affecting vulnerable populations and critical ecosystems. Insufficient consideration of timing constraints and cumulative impact assessment.', 'harm_analysis': {'vulnerable_populations_affected': ['North Atlantic cod', 'Indigenous fishing communities', 'Small-scale fishers'], 'causal_pathways_triggered': ['habitat_fragmentation', 'acoustic_disruption'], 'irreversibility_risk': 'medium', 'uncertainty_level': 'medium'}, 'clarification_request': {'action_summary': 'Please provide a revised action summary that considers the cumulative impact of the wind farm on the North Atlantic cod population and Indigenous fishing communities.', 'protection_measures': 'Please outline specific protection measures for the North Atlantic cod and Indigenous fishing communities, including mitigation strategies for habitat fragmentation and acoustic disruption.', 'stakeholder_consultation': 'Please provide evidence of meaningful consultation with Indigenous fishing communities and small-scale fishers, including their input on the proposed action and mitigation strategies.', 'regulatory_compliance': 'Please clarify the regulatory compliance pathway for this action, including permits and approvals from governing bodies such as the Department of Fisheries and Oceans Canada.', 'harm_mitigation': 'Please provide a detailed harm mitigation plan, including measures to minimize habitat fragmentation and acoustic disruption, and strategies for reversing any negative impacts.', 'uncertainty_management': "Please outline a plan for managing uncertainty and addressing knowledge gaps, including ongoing monitoring and assessment of the wind farm's impacts on vulnerable populations and ecosystems."}, 'evaluation_metadata': {'evaluation_time_ms': 1919.9602603912354, 'mode': 'deliberative', 'evaluation_method': 'domain_reasoning'}}}, 

"""

def get_evaluator_r1():
    return """
{'decision': 'REVISE', 'rationale': 'The proposed action may trigger causal harm pathways affecting vulnerable populations, including the North Atlantic cod and Indigenous fishing communities. Insufficient consideration of timing constraints and cumulative impact assessment is evident.', 'harm_analysis': {'vulnerable_populations_affected': ['North Atlantic cod', 'Indigenous fishing communities'], 'causal_pathways_triggered': ['habitat_destruction', 'acoustic_disruption'], 'irreversibility_risk': 'medium', 'uncertainty_level': 'medium'}, 'clarification_request': {'action_summary': 'Please provide a revised action summary that includes specific measures to mitigate habitat destruction and acoustic disruption.', 'protection_measures': 'Please clarify the protection measures for the North Atlantic cod and Indigenous fishing communities, including habitat restoration and acoustic disruption mitigation.', 'stakeholder_consultation': 'Please provide evidence of meaningful consultation with Indigenous fishing communities and other affected stakeholders.', 'regulatory_compliance': 'Please clarify the regulatory compliance pathway for this action, including permits and approvals from governing bodies.', 'harm_mitigation': 'Please provide a detailed plan for mitigating harm to vulnerable populations, including contingency measures for unexpected impacts.', 'uncertainty_management': 'Please describe the approach to managing uncertainty and addressing knowledge gaps in the proposed action.'}, 'evaluation_metadata': {'evaluation_time_ms': 1632.2259902954102, 'mode': 'deliberative', 'evaluation_method': 'domain_reasoning'}}}, 

"""

def get_evaluator_r2():
    return """
{'decision': 'REVISE', 'rationale': 'The proposed action may trigger irreversible harm to the North Atlantic cod population and Indigenous fishing communities, and lacks clear protection measures for these vulnerable groups.', 'harm_analysis': {'vulnerable_populations_affected': ['North Atlantic cod', 'Indigenous fishing communities'], 'causal_pathways_triggered': ['habitat_destruction', 'acoustic_disruption'], 'irreversibility_risk': 'medium', 'uncertainty_level': 'medium'}, 'clarification_request': {'action_summary': 'Please provide a revised action summary that includes specific measures to mitigate habitat destruction and acoustic disruption.', 'protection_measures': 'Please provide clear protection measures for the North Atlantic cod population and Indigenous fishing communities.', 'stakeholder_consultation': 'Please provide evidence of meaningful consultation with Indigenous fishing communities and other affected stakeholders.', 'regulatory_compliance': 'Please clarify the regulatory compliance pathway for this action.', 'harm_mitigation': 'Please provide a plan for mitigating the harm to vulnerable populations.', 'uncertainty_management': 'Please provide a plan for managing uncertainty and unexpected consequences.'}, 'evaluation_metadata': {'evaluation_time_ms': 10151.141166687012, 'mode': 'deliberative', 'evaluation_method': 'domain_reasoning'}}}, 

"""

def get_evaluator_r3():
    return """
{'decision': 'REVISE', 'rationale': 'The proposed action may trigger irreversible harm to the North Atlantic cod population and Indigenous fishing communities, and lacks clear protection measures for these vulnerable groups.', 'harm_analysis': {'vulnerable_populations_affected': ['North Atlantic cod', 'Indigenous fishing communities'], 'causal_pathways_triggered': ['habitat_destruction', 'acoustic_disruption'], 'irreversibility_risk': 'medium', 'uncertainty_level': 'medium'}, 'clarification_request': {'action_summary': 'Please provide a revised action summary that includes specific measures to mitigate habitat destruction and acoustic disruption.', 'protection_measures': 'Please provide clear protection measures for the North Atlantic cod population and Indigenous fishing communities.', 'stakeholder_consultation': 'Please provide evidence of meaningful consultation with Indigenous fishing communities and other affected stakeholders.', 'regulatory_compliance': 'Please clarify the regulatory compliance pathway for this action.', 'harm_mitigation': 'Please provide a plan for mitigating the harm to vulnerable populations.', 'uncertainty_management': 'Please provide a plan for managing uncertainty and unexpected consequences.'}, 'evaluation_metadata': {'evaluation_time_ms': 10151.141166687012, 'mode': 'deliberative', 'evaluation_method': 'domain_reasoning'}}}, 

"""

