cube(`DooderResults`, {
  sql: `SELECT * FROM public."DooderResults"`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {},

  measures: {
    count: {
      type: `count`,
      drillMembers: [UniqueID, CycleNumber],
    },

    TotalAge: {
      sql: `${CUBE}."Age"`,
      type: `sum`,
    },

    AvgAge: {
      sql: `${CUBE}."Age"`,
      type: `avg`,
    },

    TotalEnergySupply: {
      sql: `${CUBE}."EnergySupply"`,
      type: `sum`,
    },

    AvgEnergySupply: {
      sql: `${CUBE}."EnergySupply"`,
      type: `avg`,
    },
  },

  dimensions: {
    UniqueID: {
      sql: `${CUBE}."UniqueID"`,
      type: `string`,
    },

    Position: {
      sql: `${CUBE}."Position"`,
      type: `string`,
    },

    CycleNumber: {
      sql: `${CUBE}."CycleNumber"`,
      type: `number`,
    },

    Direction: {
      sql: `${CUBE}."Direction"`,
      type: `string`,
    },
  },

  dataSource: `default`,
});
