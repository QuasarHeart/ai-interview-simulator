package org.buhuiqiming.fuchuang.controller;

import org.buhuiqiming.fuchuang.service.LiveKitService;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LiveKitController {
    private  final LiveKitService liveKitService;
    public LiveKitController(LiveKitService liveKitService) {
        this.liveKitService = liveKitService;
    }

}
