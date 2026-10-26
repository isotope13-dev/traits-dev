import com.alibaba.fastjson.JSONObject;
class FastjsonParse {
    Object parse(String value) { return JSONObject.parseObject(value); }
}
