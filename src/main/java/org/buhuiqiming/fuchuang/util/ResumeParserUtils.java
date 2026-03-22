package org.buhuiqiming.fuchuang.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import lombok.extern.slf4j.Slf4j;

import java.util.StringJoiner;

@Slf4j
public class ResumeParserUtils {

    /**
     * 从腾讯云 OCR 回调 XML 中提取纯文本内容
     * @param xmlBody 原始 XML 字符串
     * @return 拼接后的纯文本
     */
    public static String extractTextFromXml(String xmlBody) {
        try {
            XmlMapper xmlMapper = new XmlMapper();
            // 将 XML 解析为树状结构
            JsonNode root = xmlMapper.readTree(xmlBody);

            //将xml中object标签的id提取出来
            try {
                String objectId = root.findValue("Object").asText().trim();
                //objectID 格式类似 avatar/.../{id}.jpg，提取id
                String id = objectId.substring(objectId.lastIndexOf("/") + 1, objectId.lastIndexOf("."));
                UserContext.set(Long.valueOf(id));
            }catch (Exception e){
                log.error("object 解析失败");
            }

            // 定位到 JobsDetail -> ResultInfo -> ObjectInfo -> ImageOCR -> text_detections
            // XML 结构，路径层级需匹配
            JsonNode detections = root.findValue("text_detections");

            StringJoiner fullText = new StringJoiner("\n");

            if (detections != null && detections.isArray()) {
                for (JsonNode node : detections) {
                    JsonNode textNode = node.get("detected_text");
                    if (textNode != null) {
                        String text = textNode.asText().trim();
                        if (!text.isEmpty()) {
                            fullText.add(text);
                        }
                    }
                }
            }
            return fullText.toString();
        } catch (Exception e) {
            log.error("解析xml失败");
            return null;
        }
    }
}