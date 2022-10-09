cube(`SimulationResults`, {
  sql: `SELECT * FROM public."SimulationResults"`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {},

  measures: {
    count: {
      type: `count`,
      drillMembers: [experimentid, cyclenumber],
    },

    DooderCount: {
      sql: `${CUBE}."DooderCount"`,
      type: `sum`,
    },

    EnergyCount: {
      sql: `${CUBE}."EnergyCount"`,
      type: `sum`,
    },

    TotalEnergySupply: {
      sql: `${CUBE}."TotalDooderEnergySupply"`,
      type: `sum`,
    },

    AvgEnergySupply: {
      sql: `${CUBE}."TotalDooderEnergySupply"`,
      type: `avg`,
    },

    AvgEnergyAge: {
      sql: `${CUBE}."AverageEnergyAge"`,
      type: `avg`,
    },
  },

  dimensions: {
    ExperimentID: {
      sql: `${CUBE}."ExperimentID"`,
      type: `string`,
    },

    CycleNumber: {
      sql: `${CUBE}."CycleNumber"`,
      type: `number`,
    },
  },

  dataSource: `default`,
});
