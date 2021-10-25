package com.example.schedulepro.ScriptRunner

import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component
import java.io.BufferedReader
import java.io.InputStreamReader



/**
 * @author: HoweverXz
 * @Date: 2021/10/25
 * ֽ�ϵ����վ�ǳ ��֪����Ҫ����
 */
@Component
class PythonScriptRunner {
    fun Schedule(name: String, password: String): String {
        try {
            var result = ""
            val args = arrayOf("python3","/DOFOR/Schedule/test.py", name, password)
            val proc = Runtime.getRuntime().exec(args) // ִ��py�ļ�
            val `in` = BufferedReader(InputStreamReader(proc.inputStream))
            var line: String? = null
            while (`in`.readLine().also { line = it } != null) {
               result = line.toString()
            }
            `in`.close()
            proc.waitFor()
            return result
        } catch (e: Exception) {
            print(e.toString())
            return e.toString()
        }
    }
}