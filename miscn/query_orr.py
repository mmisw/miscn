#
# Simple test of SPARQLWraper (http://sparql-wrapper.sourceforge.net/) to 
# perform queries against an MMI ORR SPARQL endpoint.
# Carlos Rueda, MBARI
# 2012-12-20
#
from SPARQLWrapper import SPARQLWrapper, JSON

show_original_result = True

sparql = SPARQLWrapper("http://mmisw.org/sparql")
sparql.setReturnFormat(JSON)


def do_query(description, query):
    """
    NOTE: For simplicity it is assumed that the query is a SELECT one; other 
    query kinds like CONSTRUCT, DESCRIBE would need a different handling. 
    """
    print "-"* 80  
    print "QUERY:  %s" % description
    print "SPARQL: %s" % query
    
    sparql.setQuery(query)
    
    results = sparql.query().convert()
    
    print "RESULT:"
    
    if show_original_result:
        print "." * 80
        print "%s" % str(results)
        print "." * 80
    
    # print header
    variables = results["head"]["vars"]
    print " | ".join(variables)
    
    # print values
    for result in results["results"]["bindings"]:  
        vals = [result[var]["value"] for var in variables]
        print " | ".join(vals)
        
        
do_query('Get close matches of an certain IOOS parameter',
    """
    PREFIX ioos: <http://mmisw.org/ont/ioos/parameter/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
    SELECT DISTINCT ?close_match ?prop ?value 
    WHERE { ioos:bottom_tracking_velocity skos:closeMatch ?close_match .
            ?close_match ?prop ?value .
    } 
    """)


do_query('Get CF parameters with canonical units "kg m-2". Include the definition of the term',
    """ 
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX cf: <http://mmisw.org/ont/cf/parameter/>
    SELECT ?parameter  ?definition
    WHERE { ?parameter cf:canonical_units "kg m-2".
        ?parameter skos:definition ?definition .
    }
    LIMIT 10  
    """) 
     
do_query('Get OOI Roles',
    """ 
    prefix ionrole: <http://mmisw.org/ont/ooi/ionrole/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?uri ?user_role ?description
     WHERE {      
     ?uri rdf:type            ionrole:Role.
     ?uri ionrole:User_Role   ?user_role.
     ?uri ionrole:Description ?description.
    }
    ORDER BY ?uri
    """) 



