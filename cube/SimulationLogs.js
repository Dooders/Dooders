cube(`SimulationLogs`, {
    sql: `SELECT * FROM public."SimulationLogs"`,
    
    preAggregations: {
      // Pre-Aggregations definitions go here
      // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started  
    },
    
    joins: {
      
    },
    
    measures: {
      count: {
        type: `count`,
        drillMembers: [experimentId, id, timestamp]
      },
      
      cycleNumber: {
        sql: `cycle_number`,
        type: `sum`
      }
    },
    
    dimensions: {
      experimentId: {
        sql: `experiment_id`,
        type: `string`
      },
      
      scope: {
        sql: `scope`,
        type: `string`
      },
      
      id: {
        sql: `id`,
        type: `string`,
        primaryKey: true
      },
      
      message: {
        sql: `message`,
        type: `string`
      },
      
      timestamp: {
        sql: `timestamp`,
        type: `string`
      }
    },
    
    dataSource: `default`
  });