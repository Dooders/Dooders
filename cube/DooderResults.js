cube(`DooderResults`, {
    sql: `SELECT * FROM public."DooderResults"`,
    
    preAggregations: {
      // Pre-Aggregations definitions go here
      // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started  
    },
    
    joins: {
      
    },
    
    measures: {
      count: {
        type: `count`,
        drillMembers: [uniqueid]
      },
      
      cyclenumber: {
        sql: `${CUBE}."CycleNumber"`,
        type: `sum`
      }
    },
    
    dimensions: {
      uniqueid: {
        sql: `${CUBE}."UniqueID"`,
        type: `string`
      },
      
      position: {
        sql: `${CUBE}."Position"`,
        type: `string`
      },
      
      direction: {
        sql: `${CUBE}."Direction"`,
        type: `string`
      }
    },
    
    dataSource: `default`
  });