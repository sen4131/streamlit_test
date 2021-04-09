##################
# ALL QUERIES USED
##################


qq = '''test'''
q = '''

SELECT substr(`In Home`,1,10) IHD
    ,Day
    ,`Gross Calls` 
FROM df;
'''

q2 = '''
SELECT substr(`In Home`,1,10) IHD
, SUM(`Gross Calls`)
FROM df
GROUP BY substr(`In Home`,1,10);
'''
def q3(fx_period):
    return f'''
    SELECT Day
    , ROUND(AVG(`Gross Calls`),0) as Gross_Calls
    FROM df
    WHERE Day between 1 and {fx_period}
    GROUP BY Day
    ORDER BY 1;
    '''