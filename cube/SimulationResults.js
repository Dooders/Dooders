cube(`SimulationResults`, {
    sql: `SELECT * FROM public."SimulationResults"`,
    
    preAggregations: {
      // Pre-Aggregations definitions go here
      // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started  
    },
    
    joins: {
      
    },
    
    measures: {
      count: {
        type: `count`,
        drillMembers: [experimentid]
      },
      
      cyclenumber: {
        sql: `${CUBE}."CycleNumber"`,
        type: `sum`
      },
      
      doodercount: {
        sql: `${CUBE}."DooderCount"`,
        type: `sum`
      },
      
      energycount: {
        sql: `${CUBE}."EnergyCount"`,
        type: `sum`
      }
    },
    
    dimensions: {
      experimentid: {
        sql: `${CUBE}."ExperimentID"`,
        type: `string`
      }
    },
    
    dataSource: `default`
  });