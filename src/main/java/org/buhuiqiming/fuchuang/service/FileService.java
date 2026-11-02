package org.buhuiqiming.fuchuang.service;

import jakarta.servlet.http.HttpServletRequest;

import java.net.URL;

public interface FileService {
    URL generateCOSURL(HttpServletRequest request,String dir);
}
