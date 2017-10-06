create or replace function scratch.json_num_keys (j varchar(max))
returns int
stable as $$
    import json
    try:
      arr = json.loads(j)
      return len(arr.keys())
    except:
      return 0
$$ language plpythonu;

create or replace function scratch.json_keys (j varchar(max), i int)
returns varchar(max)
stable as $$
    import json
    try:
      arr = json.loads(j)
      keys = arr.keys()
      keys.sort()
      return keys[i-1]
    except:
      return None
$$ language plpythonu;

Select
index, scratch.json_keys(annoying_json, index)
From (
  select
  index, annoying_json
  From (
    Select '{"key1": "value1", "key2": "value2","key3": "value3"}'::varchar(max) as annoying_json
  ) as a
  Cross Join (
    Select (Row_Number() Over (Order By id))::int as index From public.loans Limit 100
  ) as b
  Where index <= scratch.json_num_keys(annoying_json)
) as a
Order By index;
