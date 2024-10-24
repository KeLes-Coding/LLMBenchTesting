import json
import sys
from LLMBenchingV3 import LLMPlanExecutor
import copy

# 初始化消息列表
messages = [
    {
        "role": "system",
        "content": """As a competent planner, you are able to skillfully call the APIs and app tools I provide to create a reasonable plan based on the queries I submit.
      Your response template should be as follows:
     {
  "OrderSteps": {
    "TotalSteps": totalsteps(int), // Total number of steps, integer type
    "Step1": {
      "Description": "Find detailed information about programming courses", // Description of the purpose of this step
      "Action": "AdvanceCourseFinder({'course_id': 'programming_fundamentals_101'})", // The action to be performed, i.e., the tool to call
      "results": [ // Simulated return value from using the tool
        {
            "key1": "Programming Fundamentals 101 is an introductory course designed to provide students with the basic skills needed to understand and create simple programs.",
            "key2": "The course covers topics such as variables, data types, control structures, functions, and basic algorithms.
                    It is suitable for beginners and assumes no prior knowledge of programming."
        }
      ]
    }
  }
}""",
    },
    {
        "role": "user",
        "content": """有以下 API tools: [
GetBooksInfo	"{
  ""Query"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""The book info for which data is needed.""
  }
}"
ArxivJSON	"{
  ""authors"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Comma separated author list. Optional.""
  },
  ""keywords"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Comma separated keyword list. Optional.""
  },
  ""sort_by"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Can be one of relevance, lastUpdatedDate, and submittedDate. Optional.""
  },
  ""sort_order"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Can be either ascending or descending. Optional.""
  },
  ""start"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""Defines the index of the first returned result, using 0-based indexing. Optional.""
  },
  ""max_results"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""The number of results returned by the query, between 1 and 100. Optional.""
  }
}"
ArxivGPT	"{
  ""paper_id"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""The arXiv ID of the paper. Must be provided.""
  },
  ""max_pages"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""Maximum number of pages to return (default all). Optional.""
  }
}"
Photomath	"{
  ""locale"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""The two-letter language code parameter.""
  },
  ""image"": {
    ""type"": ""binary"",
    ""required"": false,
    ""description"": ""A picture of a math problem. The file must be in .jpg or .jpeg format and under 500KB in size.""
  }
}"
TEDTalksAPI	"{
  ""id"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""ID of a desired specific talk. Optional.""
  },
  ""from_record_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were recorded only after the provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""to_record_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were recorded only before the provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""record_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were recorded only in the exact provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""from_publish_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were published on TED.com only after the provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""to_publish_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were published on TED.com only before the provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""publish_date"": {
    ""type"": ""Date"",
    ""required"": false,
    ""description"": ""Return talks which were published on TED.com only on the exact provided date. Format: yyyy-mm-dd. Optional.""
  },
  ""min_duration"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""Return talks which their duration in seconds is at least the provided value. Optional.""
  },
  ""max_duration"": {
    ""type"": ""Number"",
    ""required"": false,
    ""description"": ""Return talks which their duration in seconds is at most the provided value. Optional.""
  },
  ""audio_lang"": {
    ""type"": ""String"",
    ""required"": false,
    ""description"": ""Return talks which their audio language is the provided language, the provided value should be the language slug according to the /audio_languages endpoint. Optional.""
  },
  ""subtitle_lang"": {
    ""type"": ""String"",
    ""required"": false,
    ""description"": ""Return talks which have subtitles in the provided language, the provided value should be the language slug according to the /subtitle_languages endpoint. Optional.""
  },
  ""speaker"": {
    ""type"": ""String"",
    ""required"": false,
    ""description"": ""Return talks which at least one of their speakers is the provided speaker, the provided value should be the speaker slug according to the /speakers endpoint. Optional.""
  },
  ""topic"": {
    ""type"": ""String"",
    ""required"": false,
    ""description"": ""Return talks which at least one of their topics is the provided topic, the provided value should be the topic slug according to the /topics endpoint. Optional.""
  }
}"
UniversityCollegeListRankings	{}
UdemyPaidCoursesForFree	"{
  ""page"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""Page number.""
  },
  ""page_size"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""Page size.""
  },
  ""query"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""Search query (python).""
  }
}"
PronunciationAssessment	"{
  ""audio_base64"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Base64 encoded audio data. Optional.""
  },
  ""audio_format"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Format of the audio. Optional.""
  },
  ""text"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Text content. Optional.""
  }
}"
AdvanceCourseFinder	"{
  ""course_id"": {
    ""type"": ""str"",
    ""required"": true,
    ""description"": ""The ID of the course.""
  }
}"
RandomWordsWithPronunciation	{}
BookInformationLibrary	"{
  ""genre"": {
    ""type"": ""str"",
    ""required"": false,
    ""description"": ""Genre of the content. Can be Fiction if provided. Optional parameter.""
  }
}"
]
返回值为：
[
    "GetBooksInfo:
{
  ""type"": ""object"",
  ""properties"": {
    ""results"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""isbn"": {
            ""type"": ""string""
          },
          ""author"": {
            ""type"": ""string""
          },
          ""description"": {
            ""type"": ""string""
          },
          ""img_link"": {
            ""type"": ""string""
          },
          ""pdf_link"": {
            ""type"": ""string""
          },
          ""publisher"": {
            ""type"": ""string""
          },
          ""title"": {
            ""type"": ""string""
          },
          ""year"": {
            ""type"": ""string""
          }
        }
      }
    }
  }
}"
"ArxivJSON:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""id"": {
        ""type"": ""string""
      },
      ""version"": {
        ""type"": ""integer""
      },
      ""published"": {
        ""type"": ""string""
      },
      ""updated"": {
        ""type"": ""string""
      },
      ""title"": {
        ""type"": ""string""
      },
      ""authors"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""name"": {
              ""type"": ""string""
            }
          }
        }
      },
      ""summary"": {
        ""type"": ""string""
      },
      ""comment"": {
        ""type"": ""string""
      },
      ""journal_ref"": {
        ""type"": ""string""
      },
      ""primary_category"": {
        ""type"": ""string""
      },
      ""links"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object""
        }
      },
      ""category"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""string""
        }
      }
    }
  }
}"
"ArxivGPT:
{
  ""type"": ""object"",
  ""properties"": {
    ""paper_id"": {
      ""type"": ""string""
    },
    ""content"": {
      ""type"": ""string""
    },
    ""total_pages"": {
      ""type"": ""integer""
    },
    ""returned_pages"": {
      ""type"": ""integer""
    },
    ""format"": {
      ""type"": ""string"",
      ""enum"": [
        ""text"",
        ""markdown""
      ]
    }
  }
}"
"Photomath:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""solution"": {
        ""type"": ""object"",
        ""properties"": {
          ""steps"": {
            ""type"": ""array"",
            ""items"": {
              ""type"": ""object"",
              ""properties"": {
                ""description"": {
                  ""type"": ""string""
                },
                ""expression"": {
                  ""type"": ""string""
                }
              }
            }
          },
          ""result"": {
            ""type"": ""string""
          }
        }
      },
      ""problem"": {
        ""type"": ""string""
      },
      ""type"": {
        ""type"": ""string""
      }
    }
  },
  ""meta"": {
    ""type"": ""object"",
    ""properties"": {
      ""confidence"": {
        ""type"": ""number""
      },
      ""timestamp"": {
        ""type"": ""string""
      }
    }
  }
}"
"TEDTalksAPI
{
  ""results"": [
    {
      ""id"": {
        ""type"": ""integer""
      },
      ""url"": {
        ""type"": ""string""
      },
      ""title"": {
        ""type"": ""string""
      },
      ""description"": {
        ""type"": ""string""
      },
      ""audio_language"": {
        ""type"": ""string""
      },
      ""event"": {
        ""type"": ""string""
      },
      ""publish_date"": {
        ""type"": ""string""
      },
      ""record_date"": {
        ""type"": ""string""
      },
      ""duration_in_seconds"": {
        ""type"": ""integer""
      },
      ""thumbnail_url"": {
        ""type"": ""string""
      },
      ""mp4_url"": {
        ""type"": ""string""
      },
      ""embed_url"": {
        ""type"": ""string""
      }
    }
  ]
}"
"UniversityCollegeListRankings:
{
  ""universities"": [
    {
      ""id"": {
        ""type"": ""integer""
      },
      ""name"": {
        ""type"": ""string""
      },
      ""country"": {
        ""type"": ""string""
      },
      ""city"": {
        ""type"": ""string""
      },
      ""rank"": {
        ""type"": ""integer""
      },
      ""overall_score"": {
        ""type"": ""number""
      },
      ""teaching_score"": {
        ""type"": ""number""
      },
      ""research_score"": {
        ""type"": ""number""
      },
      ""citations_score"": {
        ""type"": ""number""
      },
      ""industry_income_score"": {
        ""type"": ""number""
      },
      ""international_outlook_score"": {
        ""type"": ""number""
      },
      ""website"": {
        ""type"": ""string""
      },
      ""logo_url"": {
        ""type"": ""string""
      }
    }
  ]
}"
"UdemyPaidCoursesForFree:
{
  ""type"": ""object"",
  ""properties"": {
    ""courses"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""name"": {
            ""type"": ""string""
          },
          ""category"": {
            ""type"": ""string""
          },
          ""image"": {
            ""type"": ""string""
          },
          ""actual_price_usd"": {
            ""type"": ""number""
          },
          ""sale_price_usd"": {
            ""type"": ""number""
          },
          ""sale_end"": {
            ""type"": ""string""
          },
          ""description"": {
            ""type"": ""string""
          },
          ""url"": {
            ""type"": ""string""
          },
          ""clean_url"": {
            ""type"": ""string""
          }
        }
      }
    }
  }
}"
"PronunciationAssessment：
{
  ""words"": [
    {
      ""label"": {
        ""type"": ""string""
      },
      ""phones"": [
        {
          ""label"": {
            ""type"": ""string""
          },
          ""label_ipa"": {
            ""type"": ""string""
          },
          ""confidence"": {
            ""type"": ""integer""
          },
          ""score"": {
            ""type"": ""integer""
          },
          ""error"": {
            ""type"": ""boolean""
          },
          ""sounds_like"": [
            {
              ""label"": {
                ""type"": ""string""
              },
              ""label_ipa"": {
                ""type"": ""string""
              },
              ""confidence"": {
                ""type"": ""integer""
              }
            },
            {
              ""label"": {
                ""type"": ""string""
              },
              ""label_ipa"": {
                ""type"": ""string""
              },
              ""confidence"": {
                ""type"": ""integer""
              }
            },
            {
              ""label"": {
                ""type"": ""string""
              },
              ""label_ipa"": {
                ""type"": ""string""
              },
              ""confidence"": {
                ""type"": ""integer""
              }
            }
          ]
        }
      ],
      ""score"": {
        ""type"": ""integer""
      }
    }
  ]
}"
"AdvanceCourseFinder:
{
  ""type"": ""object"",
  ""properties"": {
    ""key1"": {
      ""type"": ""string""
    },
    ""key2"": {
      ""type"": ""string""
    }
  }
}"
"RandomWordsWithPronunciation:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""definition"": {
        ""type"": ""string""
      },
      ""pronunciation"": {
        ""type"": ""string""
      },
      ""word"": {
        ""type"": ""string""
      }
    }
  }
}"
"BookInformationLibrary:
{
  ""type"": ""object"",
  ""properties"": {
    ""totalBooks"": {
      ""type"": ""integer""
    },
    ""recommendations"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""_id"": {
            ""type"": ""string""
          },
          ""title"": {
            ""type"": ""string""
          },
          ""author"": {
            ""type"": ""string""
          },
          ""genre"": {
            ""type"": ""string""
          },
          ""summary"": {
            ""type"": ""string""
          },
          ""img_url"": {
            ""type"": ""string""
          },
          ""reviews"": {
            ""type"": ""array"",
            ""items"": {
              ""type"": ""object"",
              ""properties"": {
                ""reviewer"": {
                  ""type"": ""string""
                },
                ""rating"": {
                  ""type"": ""integer""
                },
                ""comment"": {
                  ""type"": ""string""
                },
                ""_id"": {
                  ""type"": ""string""
                }
              }
            }
          },
          ""__v"": {
            ""type"": ""integer""
          }
        }
      }
    }
  }
}"
]
任务是:""",
    },
]


def main():
    # 从命令行参数中获取message
    message_json = sys.argv[1]
    query_message = json.loads(message_json)

    # 打印message
    print("Received message:")
    # for msg in message:
    #     print(msg)
    print(query_message)

    combined_messages = copy.deepcopy(messages)
    combined_messages[-1]["content"] += query_message

    print(combined_messages)

    executor = LLMPlanExecutor()
    executor.messages = combined_messages
    executor.execute_plan()


if __name__ == "__main__":
    main()
