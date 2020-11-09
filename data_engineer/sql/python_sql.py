    
 def schema_database(df, name, cursor, drop=True):
    """"
    df -> database pandas
    name -> nome da tabela do bando de dados
    cursos -> conecao com o banco de dados
    drop -> se vai ou nao deletar o banco de dados antes de criar
    """"
    fields = ""
    types = {
        'int64': 'BIGINT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'datetime64[ns]': 'TIMESTAMP',
        'datetime64[ns, UTC]': 'TIMESTAMP',
        'bool': 'BOOLEAN',
    }

    index = 0
    for col in df.columns:
        field = col+' '+types[str(df.dtypes[index])]+' NULL,'
        fields = fields + field
        index = index + 1
    fields = fields[:len(fields)-1]
    # print(fields)
    # print(" ")
    print("CLEANING DATABASE...")
    if drop:
        drop_string = 'drop table if exists '+name+';'
        print(drop_string)
    else:
        drop_string = ''

    cursor.execute("""
        """+drop_string+"""

        CREATE TABLE IF NOT EXISTS """+name+"""
        (
        """+fields+"""
        );
    """)