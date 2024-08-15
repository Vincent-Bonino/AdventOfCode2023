use crate::day05::models::{Mapping, Range};

fn build_test_mapping() -> Mapping {
    Mapping::new(
        200,
        100,
        50,
    )
}

#[test]
fn test_map_range_included() {
    let mapping: Mapping = build_test_mapping();
    let tst_range: Range = Range { start: 110, end: 120 };

    let expected: (Vec<Range>, Vec<Range>) = (  // not mapped, mapped
        vec![],
        vec![ Range::from_length(210, 10) ],
    );

    assert_eq!(expected, mapping.map_seed_range(tst_range))
}

#[test]
fn test_map_range_including() {
    let mapping: Mapping = build_test_mapping();
    let tst_range: Range = Range { start: 90, end: 160 };

    let expected: (Vec<Range>, Vec<Range>) = (  // not mapped, mapped
        vec![ Range::from_length(90, 10), Range::from_length(150, 10) ],
        vec![ Range::from_length(200, 50) ],
    );

    assert_eq!(expected, mapping.map_seed_range(tst_range))
}

#[test]
fn test_map_range_left() {
    let mapping: Mapping = build_test_mapping();
    let tst_range: Range = Range { start: 80, end: 120 };

    let expected: (Vec<Range>, Vec<Range>) = (  // not mapped, mapped
        vec![ Range::from_length(80, 20)],
        vec![ Range::from_length(200, 20) ],
    );

    assert_eq!(expected, mapping.map_seed_range(tst_range))
}

#[test]
fn test_overlap() {
    let range_ref: Range = Range::from_length(0,100);

    let range1: Range = Range::from_length(25, 50);
    let range2: Range = Range::from_length(-100, 300);
    let range3: Range = Range::from_length(500, 100);

    assert!(range_ref.overlap_with(&range1));
    assert!(range_ref.overlap_with(&range2));
    assert!(!range_ref.overlap_with(&range3));
}
