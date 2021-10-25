package com.example.schedulepro.Controller

import com.example.schedulepro.Model.ScheduleModel
import com.example.schedulepro.ScriptRunner.PythonScriptRunner
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.*

/**
@author: HoweverXz
@Date: 2021/10/24
纸上得来终觉浅 绝知此事要躬行
 */
//暂时使用kotlin处理 会换成golang
@CrossOrigin
@RestController
class ScheduleInfoController {
    @Autowired
    lateinit var runner: PythonScriptRunner

    @PostMapping("/infos")
    fun getScheduleInfo(@RequestBody userinfo: ScheduleModel):String {
        try {
            var name = userinfo.name
            var password = userinfo.password
            val schedule = runner.Schedule(name, password)
            return schedule
        } catch (e: Exception) {
            return e.toString()
        }
    }
}