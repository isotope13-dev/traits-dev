import HealthKit

let query = HKSampleQuery(sampleType: sampleType, predicate: nil, limit: 1, sortDescriptors: nil) { _, _, _ in }
let statistics = HKStatisticsQuery(quantityType: quantityType, quantitySamplePredicate: nil, options: []) { _, _, _ in }
let anchored = HKAnchoredObjectQuery(type: sampleType, predicate: nil, anchor: nil, limit: 1) { _, _, _, _, _ in }
