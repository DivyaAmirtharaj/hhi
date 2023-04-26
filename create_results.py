import datetime
import getpass
from clustering import Clustering

def run_cluster():
    j = Clustering([785919], k_value=3, section_name="Justice")
    j.run()
    write_cluster_results(j.section_name, f"{j.qids}", j.response_breakdown, j.similar, j.demographic_summary, j.cluster_dict, j.cluster_demographics, j.section_name+".png")

    o = Clustering([972241, 898570], k_value=2, section_name="Optimism")
    o.run()
    write_cluster_results(o.section_name, f"{o.qids}", o.response_breakdown, o.similar, o.demographic_summary, o.cluster_dict, o.cluster_demographics, o.section_name+".png")
    
    a = Clustering([458111, 243034, 245609, 174244], k_value=2, section_name="Accountability")
    a.run()
    write_cluster_results(a.section_name, f"{a.qids}", a.response_breakdown, a.similar, a.demographic_summary, a.cluster_dict, a.cluster_demographics, a.section_name+".png")

def write_cluster_results(section, qids, response_breakdown, cluster_descriptions, demographics, cluster_dict, cluster_demographics, graph_name):
    # Define the values to substitute
    values = {
        'date': datetime.date.today(),
        'time': datetime.datetime.now().strftime("%H%M%S"),
        'author': getpass.getuser(),
        'dataset': 'dedoose_data',
        'section': section,
        'qids': qids,
        'response_breakdown': response_breakdown,
        'cluster_descriptions': cluster_descriptions,
        'demographics': demographics,
        'cluster_dict': cluster_dict,
        'cluster_demographics': cluster_demographics,
        'graph_name': graph_name
    }

    # Load the template from a file
    with open('sample_cluster_results.md', 'r') as f:
        template = f.read()
    
    output_file = f"{section}_cluster_report.md"
    # Substitute the values into the template
    report = template.format(output_file=output_file, **values)
    # Write the report to a file with the unique name
    with open(output_file, 'w') as f:
        f.write(report)

def write_theme_results(section, keywords, themes, analysis_questions):
    # Define the values to substitute
    values = {
        'date': datetime.date.today(),
        'time': datetime.datetime.now().strftime("%H%M%S"),
        'author': getpass.getuser(),
        'dataset': 'dedoose_data',
        'section': section,
        'keywords': keywords,
        'themes': themes,
        'analysis_questions': analysis_questions,
    }

    # Load the template from a file
    with open('sample_cluster_results.md', 'r') as f:
        template = f.read()
    
    output_file = f"{section}_cluster_report.md"
    # Substitute the values into the template
    report = template.format(output_file=output_file, **values)
    # Write the report to a file with the unique name
    with open(output_file, 'w') as f:
        f.write(report)
#run_cluster()
