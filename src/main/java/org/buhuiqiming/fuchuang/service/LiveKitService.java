package org.buhuiqiming.fuchuang.service;

import java.io.IOException;
import java.util.Map;

public interface LiveKitService {
    public Map<String, String> startAutoInterview(String interviewId) throws IOException;
}
