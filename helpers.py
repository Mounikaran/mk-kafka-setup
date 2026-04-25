from bson.json_util import dumps


def change_response_format(response):
    resp_obj = {
        "mongoId": str(response.get("_id") or ""),
        "org": response.get("org") or "",
        "uuid": response.get("uuid") or "",
        "projectId": response.get("projectId") or "",
        "surveyId": response.get("surveyId") or "",
        "collectorId": response.get("collectorId") or "",
        "collectorType": max(int(response.get("collectorType",-1)), -1),
        "eMsgId": str(response.get("eMsgId") or ""),
        "eMsgDataId": str(response.get("eMsgDataId") or ""),
        "status": response.get("status") or "",
        "answers": [],
        "embedDataArr": response.get("embedDataArr") or [],
        "embedData": dumps(response.get("embedData") or {}),
        "surveyVersion": response.get("surveyVersion") or 1,
        "fieldForceVersion": response.get("fieldForceVersion") or "",
        "agentId": str(response.get("agentId") or ""),
        "ticketIds": response.get("ticketIds") or [],
        "disqQuesId": response.get("disqQuesId") or "",
        "geoLocation": dumps(response.get("geoLocation") or {}),
        "thankYouClicks": {
            "facebook": response.get("thankYouClicks", {}).get("facebook") or 0,
            "linkedIn": response.get("thankYouClicks", {}).get("linkedIn") or 0,
            "whatsapp": response.get("thankYouClicks", {}).get("whatsapp") or 0,
            "twitter": response.get("thankYouClicks", {}).get("twitter") or 0,
        },
        "userAgent": response.get("userAgent") or "",
        "deviceInfo": response.get("deviceInfo") or {},
        "ipAddress": response.get("ipAddress") or "",
        "preview": response.get("preview") or False,
        "isEdited": response.get("isEdited") or False,
        "testLink": response.get("testLink") or False,
        "editHistory": response.get("editHistory") or None,
        "qualityFlags": dumps(response.get("qualityFlags") or {}),
        "loopFlow": dumps(response.get("loopFlow") or {}),
        "maxDifferenceFlow": dumps(response.get("maxDifferenceFlow") or {}),
        "pageNavigation": dumps(response.get("pageNavigation") or {}),
        "timer": dumps(response.get("timer") or {}),
        "textAnalysis": dumps(response.get("textAnalysis") or {}),
        "currentPageDetails": dumps(response.get("currentPageDetails") or {}),
        "audioRecordings": dumps(response.get("audioRecordings") or {}),
        "submittedAt": str(response.get("submittedAt") or ""),
        "created": str(response.get("createdAt") or ""),
        "modified": str(response.get("updatedAt") or ""),
        "isListed": response.get("isListed") or False,
        "hasActions": True,
        "quotaDoc": response.get("quotaDoc") or [],
        "panelguid": response.get("panelguid") or "",
        "panelistData": dumps(response.get("panelistData") or {}),
        "usabilityTestingTime": response.get("usabilityTestingTime") or -1,
    }
    if response.get("answers") and isinstance(response["answers"], dict):
        resp_obj["answers"] = [
            {
                "questionId": key,
                "value": dumps(ans),
            }
            for key, ans in response["answers"].items()
        ]
    device_info = resp_obj.get("deviceInfo") or None
    if device_info and not device_info.get("type"):
        resp_obj["deviceInfo"] = None
    elif device_info and isinstance(device_info, dict):
        device_info["os"] = response.get("deviceInfo", {}).get("os") or ""
        device_info["browser"] = response.get("deviceInfo", {}).get("browser") or ""
    resp_obj["deviceInfo"] = device_info
    return resp_obj
