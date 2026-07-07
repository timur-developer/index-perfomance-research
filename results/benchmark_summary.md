# Benchmark summary

Summary statistics are calculated from measured runs only.

| DBMS | Index config | Query | Median, ms | Mean, ms | Min, ms | Max, ms | Std, ms | p95, ms | p99, ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| mongo | all_indexes | Q1: Exact search by student_id | 0.661 | 0.668 | 0.445 | 1.210 | 0.141 | 0.931 | 1.100 |
| mongo | all_indexes | Q2: Date range filtering by created_at | 11.418 | 11.744 | 8.715 | 17.327 | 1.679 | 14.870 | 15.917 |
| mongo | all_indexes | Q3: Low-selectivity filtering by status | 55.574 | 56.598 | 45.645 | 78.838 | 4.764 | 64.951 | 75.262 |
| mongo | all_indexes | Q4: Combined filtering by status and created_at | 3.243 | 3.312 | 2.214 | 5.725 | 0.549 | 4.351 | 5.084 |
| mongo | all_indexes | Q5: Sort by created_at DESC with LIMIT | 0.685 | 0.694 | 0.473 | 1.849 | 0.128 | 0.915 | 1.036 |
| mongo | all_indexes | Q6: Aggregation by course_id for graded activities | 415.980 | 419.027 | 382.629 | 540.244 | 21.041 | 453.031 | 513.672 |
| mongo | all_indexes | Q7: Broad score range where indexes are expected to help little | 438.574 | 444.955 | 397.344 | 634.633 | 29.987 | 495.310 | 582.624 |
| mongo | idx_course_score_only | Q1: Exact search by student_id | 312.732 | 315.296 | 279.306 | 417.613 | 18.161 | 343.973 | 395.251 |
| mongo | idx_course_score_only | Q2: Date range filtering by created_at | 378.510 | 382.036 | 339.222 | 536.760 | 22.920 | 417.155 | 489.576 |
| mongo | idx_course_score_only | Q3: Low-selectivity filtering by status | 342.816 | 347.009 | 305.570 | 503.089 | 24.527 | 387.658 | 450.807 |
| mongo | idx_course_score_only | Q4: Combined filtering by status and created_at | 412.050 | 415.071 | 372.701 | 573.738 | 22.952 | 448.898 | 513.499 |
| mongo | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 438.970 | 443.576 | 395.524 | 636.386 | 27.964 | 485.681 | 571.188 |
| mongo | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 518.863 | 522.980 | 470.840 | 688.057 | 27.506 | 563.985 | 636.903 |
| mongo | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 440.923 | 445.648 | 386.933 | 660.082 | 28.777 | 486.191 | 577.619 |
| mongo | idx_created_at_only | Q1: Exact search by student_id | 303.314 | 307.232 | 274.845 | 423.262 | 20.034 | 342.084 | 394.012 |
| mongo | idx_created_at_only | Q2: Date range filtering by created_at | 12.008 | 12.158 | 9.190 | 17.319 | 1.524 | 14.887 | 15.970 |
| mongo | idx_created_at_only | Q3: Low-selectivity filtering by status | 337.091 | 339.756 | 308.470 | 456.248 | 20.108 | 371.958 | 425.287 |
| mongo | idx_created_at_only | Q4: Combined filtering by status and created_at | 121.983 | 125.395 | 106.844 | 183.308 | 12.316 | 151.159 | 173.488 |
| mongo | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 0.679 | 0.711 | 0.460 | 1.621 | 0.159 | 0.999 | 1.198 |
| mongo | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 527.860 | 534.755 | 476.803 | 807.580 | 33.790 | 582.117 | 685.020 |
| mongo | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 438.755 | 443.577 | 402.731 | 626.289 | 25.068 | 480.165 | 551.886 |
| mongo | idx_status_created_at_only | Q1: Exact search by student_id | 302.386 | 305.535 | 267.422 | 410.090 | 18.486 | 335.544 | 380.368 |
| mongo | idx_status_created_at_only | Q2: Date range filtering by created_at | 368.649 | 373.125 | 334.532 | 529.533 | 24.279 | 412.095 | 482.865 |
| mongo | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 57.567 | 58.646 | 46.885 | 87.550 | 5.247 | 68.631 | 78.041 |
| mongo | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 3.205 | 3.288 | 2.168 | 6.207 | 0.567 | 4.360 | 5.026 |
| mongo | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 435.896 | 439.863 | 398.029 | 600.322 | 25.394 | 479.787 | 563.140 |
| mongo | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 775.598 | 786.195 | 709.289 | 1202.243 | 46.626 | 857.638 | 969.747 |
| mongo | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 437.077 | 442.872 | 398.603 | 679.870 | 29.489 | 489.915 | 572.617 |
| mongo | idx_status_only | Q1: Exact search by student_id | 302.737 | 306.779 | 272.540 | 445.993 | 21.443 | 344.017 | 408.611 |
| mongo | idx_status_only | Q2: Date range filtering by created_at | 369.594 | 375.586 | 332.392 | 523.963 | 25.486 | 419.386 | 494.030 |
| mongo | idx_status_only | Q3: Low-selectivity filtering by status | 56.084 | 57.177 | 43.039 | 87.258 | 5.161 | 66.997 | 76.144 |
| mongo | idx_status_only | Q4: Combined filtering by status and created_at | 318.043 | 320.634 | 288.903 | 420.421 | 17.105 | 348.130 | 402.855 |
| mongo | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 439.777 | 444.521 | 402.403 | 613.572 | 25.743 | 481.948 | 569.522 |
| mongo | idx_status_only | Q6: Aggregation by course_id for graded activities | 417.505 | 421.319 | 385.273 | 559.525 | 21.602 | 457.239 | 518.004 |
| mongo | idx_status_only | Q7: Broad score range where indexes are expected to help little | 436.856 | 442.150 | 399.363 | 630.432 | 28.426 | 485.583 | 577.758 |
| mongo | idx_student_id_only | Q1: Exact search by student_id | 0.686 | 0.713 | 0.439 | 2.094 | 0.179 | 1.040 | 1.291 |
| mongo | idx_student_id_only | Q2: Date range filtering by created_at | 371.888 | 378.296 | 333.190 | 520.922 | 26.169 | 425.530 | 492.974 |
| mongo | idx_student_id_only | Q3: Low-selectivity filtering by status | 336.543 | 340.345 | 301.908 | 465.363 | 20.789 | 378.666 | 425.050 |
| mongo | idx_student_id_only | Q4: Combined filtering by status and created_at | 406.235 | 410.648 | 368.411 | 581.877 | 25.630 | 444.568 | 531.702 |
| mongo | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 445.016 | 448.957 | 403.924 | 603.258 | 23.945 | 484.729 | 558.932 |
| mongo | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 537.447 | 543.206 | 486.067 | 798.664 | 32.300 | 590.532 | 692.833 |
| mongo | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 440.762 | 444.633 | 404.198 | 591.258 | 24.316 | 484.382 | 560.215 |
| mongo | no_indexes | Q1: Exact search by student_id | 315.514 | 319.231 | 276.655 | 446.660 | 21.411 | 361.031 | 403.658 |
| mongo | no_indexes | Q2: Date range filtering by created_at | 385.236 | 389.489 | 327.748 | 513.206 | 26.511 | 439.459 | 485.598 |
| mongo | no_indexes | Q3: Low-selectivity filtering by status | 347.649 | 350.994 | 288.748 | 479.180 | 22.706 | 388.440 | 440.081 |
| mongo | no_indexes | Q4: Combined filtering by status and created_at | 411.954 | 414.990 | 352.036 | 545.772 | 27.302 | 463.201 | 516.462 |
| mongo | no_indexes | Q5: Sort by created_at DESC with LIMIT | 457.091 | 462.936 | 411.420 | 644.672 | 31.050 | 518.514 | 581.597 |
| mongo | no_indexes | Q6: Aggregation by course_id for graded activities | 564.381 | 568.457 | 482.888 | 742.838 | 38.480 | 639.732 | 698.210 |
| mongo | no_indexes | Q7: Broad score range where indexes are expected to help little | 449.374 | 457.003 | 349.679 | 690.359 | 34.952 | 526.446 | 592.078 |
| mysql | all_indexes | Q1: Exact search by student_id | 15.448 | 15.569 | 4.506 | 31.071 | 3.738 | 24.852 | 29.311 |
| mysql | all_indexes | Q2: Date range filtering by created_at | 31.066 | 29.970 | 11.798 | 37.667 | 4.702 | 33.478 | 34.730 |
| mysql | all_indexes | Q3: Low-selectivity filtering by status | 62.017 | 59.514 | 39.016 | 69.008 | 6.665 | 64.642 | 66.841 |
| mysql | all_indexes | Q4: Combined filtering by status and created_at | 31.038 | 28.505 | 8.258 | 41.109 | 6.653 | 32.603 | 33.353 |
| mysql | all_indexes | Q5: Sort by created_at DESC with LIMIT | 16.196 | 19.846 | 5.778 | 33.684 | 7.909 | 31.239 | 32.096 |
| mysql | all_indexes | Q6: Aggregation by course_id for graded activities | 305.214 | 305.660 | 267.846 | 363.390 | 12.648 | 326.034 | 344.083 |
| mysql | all_indexes | Q7: Broad score range where indexes are expected to help little | 157.299 | 157.154 | 136.957 | 185.305 | 7.791 | 169.645 | 177.565 |
| mysql | idx_course_score_only | Q1: Exact search by student_id | 125.522 | 126.663 | 108.758 | 173.760 | 8.245 | 140.218 | 153.147 |
| mysql | idx_course_score_only | Q2: Date range filtering by created_at | 155.540 | 154.356 | 133.914 | 186.095 | 8.131 | 166.271 | 175.046 |
| mysql | idx_course_score_only | Q3: Low-selectivity filtering by status | 156.502 | 156.633 | 136.472 | 204.486 | 9.067 | 171.750 | 185.458 |
| mysql | idx_course_score_only | Q4: Combined filtering by status and created_at | 188.714 | 188.949 | 164.900 | 247.857 | 9.346 | 205.338 | 215.035 |
| mysql | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 248.722 | 249.628 | 222.346 | 352.277 | 12.754 | 270.063 | 296.497 |
| mysql | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 2254.929 | 2517.145 | 1897.660 | 4863.650 | 554.581 | 3619.681 | 4165.188 |
| mysql | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 155.713 | 155.849 | 136.284 | 224.845 | 10.928 | 172.029 | 196.570 |
| mysql | idx_created_at_only | Q1: Exact search by student_id | 124.087 | 122.786 | 107.985 | 154.813 | 6.386 | 131.047 | 136.780 |
| mysql | idx_created_at_only | Q2: Date range filtering by created_at | 30.864 | 28.160 | 11.674 | 37.157 | 7.096 | 34.193 | 35.555 |
| mysql | idx_created_at_only | Q3: Low-selectivity filtering by status | 155.388 | 153.593 | 133.942 | 177.686 | 7.098 | 161.048 | 167.135 |
| mysql | idx_created_at_only | Q4: Combined filtering by status and created_at | 115.156 | 115.655 | 97.086 | 147.108 | 8.165 | 127.022 | 136.088 |
| mysql | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 15.508 | 16.220 | 5.084 | 42.658 | 4.877 | 27.006 | 30.706 |
| mysql | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 263.955 | 264.255 | 236.547 | 312.763 | 9.974 | 280.641 | 291.619 |
| mysql | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 139.958 | 138.580 | 119.828 | 167.827 | 6.454 | 145.820 | 150.371 |
| mysql | idx_status_created_at_only | Q1: Exact search by student_id | 124.583 | 124.413 | 108.427 | 149.516 | 5.933 | 134.190 | 140.547 |
| mysql | idx_status_created_at_only | Q2: Date range filtering by created_at | 30.915 | 29.560 | 14.373 | 41.774 | 4.847 | 32.800 | 34.401 |
| mysql | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 61.837 | 59.816 | 38.769 | 82.902 | 6.347 | 64.797 | 69.044 |
| mysql | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 30.767 | 27.577 | 7.974 | 42.024 | 7.385 | 32.226 | 33.032 |
| mysql | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 246.392 | 245.662 | 221.663 | 285.199 | 8.970 | 258.726 | 269.814 |
| mysql | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 649.829 | 656.079 | 591.764 | 887.883 | 35.417 | 719.530 | 762.553 |
| mysql | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 140.575 | 140.430 | 120.469 | 173.417 | 7.864 | 152.649 | 161.227 |
| mysql | idx_status_only | Q1: Exact search by student_id | 124.375 | 123.768 | 108.325 | 150.158 | 6.243 | 133.368 | 140.112 |
| mysql | idx_status_only | Q2: Date range filtering by created_at | 155.692 | 154.727 | 132.440 | 217.744 | 8.065 | 165.167 | 176.198 |
| mysql | idx_status_only | Q3: Low-selectivity filtering by status | 61.502 | 58.952 | 38.663 | 108.260 | 7.627 | 66.435 | 72.804 |
| mysql | idx_status_only | Q4: Combined filtering by status and created_at | 253.769 | 255.235 | 229.612 | 315.953 | 10.812 | 275.459 | 290.282 |
| mysql | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 248.911 | 248.413 | 223.044 | 297.852 | 9.111 | 262.472 | 272.933 |
| mysql | idx_status_only | Q6: Aggregation by course_id for graded activities | 313.778 | 317.894 | 284.208 | 470.356 | 19.939 | 354.654 | 391.148 |
| mysql | idx_status_only | Q7: Broad score range where indexes are expected to help little | 140.267 | 140.245 | 122.255 | 186.537 | 8.000 | 152.880 | 162.046 |
| mysql | idx_student_id_only | Q1: Exact search by student_id | 15.395 | 15.335 | 4.358 | 28.273 | 4.155 | 25.196 | 26.729 |
| mysql | idx_student_id_only | Q2: Date range filtering by created_at | 155.483 | 154.037 | 132.987 | 189.145 | 7.049 | 161.806 | 168.419 |
| mysql | idx_student_id_only | Q3: Low-selectivity filtering by status | 155.737 | 155.961 | 134.864 | 214.121 | 8.842 | 171.062 | 185.217 |
| mysql | idx_student_id_only | Q4: Combined filtering by status and created_at | 186.485 | 186.226 | 162.303 | 308.413 | 10.767 | 200.712 | 214.465 |
| mysql | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 243.671 | 243.322 | 221.138 | 279.840 | 9.263 | 258.519 | 266.093 |
| mysql | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 257.408 | 259.101 | 234.286 | 316.526 | 11.907 | 282.109 | 293.080 |
| mysql | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 139.983 | 138.425 | 120.332 | 175.146 | 6.988 | 146.433 | 152.902 |
| mysql | no_indexes | Q1: Exact search by student_id | 124.612 | 124.568 | 107.902 | 153.677 | 5.977 | 134.452 | 142.719 |
| mysql | no_indexes | Q2: Date range filtering by created_at | 154.891 | 152.621 | 131.496 | 184.109 | 7.223 | 160.230 | 167.671 |
| mysql | no_indexes | Q3: Low-selectivity filtering by status | 155.457 | 154.929 | 133.675 | 193.552 | 6.907 | 163.503 | 173.645 |
| mysql | no_indexes | Q4: Combined filtering by status and created_at | 186.727 | 186.345 | 162.407 | 219.549 | 6.876 | 196.157 | 203.327 |
| mysql | no_indexes | Q5: Sort by created_at DESC with LIMIT | 247.608 | 247.323 | 221.224 | 300.414 | 10.424 | 264.142 | 276.182 |
| mysql | no_indexes | Q6: Aggregation by course_id for graded activities | 268.423 | 269.371 | 237.986 | 370.989 | 11.002 | 287.580 | 302.752 |
| mysql | no_indexes | Q7: Broad score range where indexes are expected to help little | 139.969 | 139.006 | 119.795 | 168.805 | 5.924 | 145.038 | 153.237 |
| postgres | all_indexes | Q1: Exact search by student_id | 30.913 | 29.951 | 14.314 | 44.501 | 4.091 | 33.364 | 34.247 |
| postgres | all_indexes | Q2: Date range filtering by created_at | 30.948 | 30.614 | 16.931 | 45.182 | 4.288 | 37.349 | 43.354 |
| postgres | all_indexes | Q3: Low-selectivity filtering by status | 46.559 | 45.489 | 25.531 | 56.151 | 4.914 | 49.476 | 51.010 |
| postgres | all_indexes | Q4: Combined filtering by status and created_at | 30.763 | 29.691 | 15.238 | 45.392 | 4.588 | 34.209 | 39.565 |
| postgres | all_indexes | Q5: Sort by created_at DESC with LIMIT | 30.785 | 29.903 | 14.539 | 44.879 | 4.125 | 33.630 | 35.141 |
| postgres | all_indexes | Q6: Aggregation by course_id for graded activities | 124.926 | 125.418 | 105.606 | 158.043 | 5.780 | 135.014 | 144.399 |
| postgres | all_indexes | Q7: Broad score range where indexes are expected to help little | 77.922 | 77.915 | 61.595 | 94.084 | 4.071 | 83.207 | 91.422 |
| postgres | idx_course_score_only | Q1: Exact search by student_id | 80.808 | 83.655 | 66.996 | 108.404 | 7.544 | 94.113 | 98.144 |
| postgres | idx_course_score_only | Q2: Date range filtering by created_at | 108.483 | 107.009 | 85.687 | 147.666 | 6.379 | 113.714 | 120.668 |
| postgres | idx_course_score_only | Q3: Low-selectivity filtering by status | 108.892 | 107.948 | 87.946 | 135.717 | 5.710 | 113.563 | 120.292 |
| postgres | idx_course_score_only | Q4: Combined filtering by status and created_at | 108.747 | 107.754 | 86.480 | 134.061 | 5.535 | 113.028 | 120.529 |
| postgres | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 187.221 | 187.004 | 166.344 | 216.735 | 5.806 | 194.415 | 207.219 |
| postgres | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 139.367 | 138.505 | 115.887 | 199.067 | 7.660 | 147.778 | 162.180 |
| postgres | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 78.141 | 78.649 | 61.535 | 117.719 | 5.814 | 89.912 | 95.664 |
| postgres | idx_created_at_only | Q1: Exact search by student_id | 92.350 | 90.377 | 67.293 | 114.534 | 7.138 | 98.527 | 105.031 |
| postgres | idx_created_at_only | Q2: Date range filtering by created_at | 30.794 | 29.447 | 14.899 | 62.063 | 4.950 | 33.009 | 35.366 |
| postgres | idx_created_at_only | Q3: Low-selectivity filtering by status | 108.755 | 108.067 | 87.803 | 141.254 | 5.706 | 113.627 | 122.461 |
| postgres | idx_created_at_only | Q4: Combined filtering by status and created_at | 60.678 | 57.103 | 37.848 | 78.789 | 7.420 | 64.334 | 67.158 |
| postgres | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 30.883 | 29.159 | 12.834 | 40.627 | 5.435 | 33.052 | 34.843 |
| postgres | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 139.704 | 138.741 | 116.493 | 191.831 | 7.316 | 147.693 | 163.177 |
| postgres | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 110.540 | 113.170 | 97.552 | 145.990 | 7.018 | 124.751 | 128.629 |
| postgres | idx_status_created_at_only | Q1: Exact search by student_id | 80.947 | 84.175 | 67.456 | 107.607 | 7.563 | 94.497 | 97.346 |
| postgres | idx_status_created_at_only | Q2: Date range filtering by created_at | 62.252 | 61.372 | 43.469 | 78.281 | 4.583 | 65.272 | 68.971 |
| postgres | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 46.525 | 45.369 | 29.816 | 58.750 | 4.590 | 48.921 | 50.943 |
| postgres | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 30.974 | 29.634 | 13.381 | 45.465 | 4.943 | 32.973 | 34.494 |
| postgres | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 187.215 | 187.376 | 166.760 | 247.561 | 6.212 | 195.087 | 210.007 |
| postgres | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 124.934 | 125.461 | 108.079 | 181.469 | 6.420 | 136.595 | 145.323 |
| postgres | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 110.767 | 113.629 | 97.428 | 158.571 | 7.383 | 125.054 | 130.871 |
| postgres | idx_status_only | Q1: Exact search by student_id | 82.044 | 84.220 | 67.500 | 104.485 | 7.556 | 94.794 | 97.243 |
| postgres | idx_status_only | Q2: Date range filtering by created_at | 108.641 | 107.206 | 86.128 | 136.399 | 6.059 | 113.048 | 120.545 |
| postgres | idx_status_only | Q3: Low-selectivity filtering by status | 46.397 | 43.933 | 23.839 | 53.478 | 6.582 | 48.441 | 49.880 |
| postgres | idx_status_only | Q4: Combined filtering by status and created_at | 93.643 | 93.458 | 74.062 | 133.599 | 5.596 | 101.092 | 111.456 |
| postgres | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 187.064 | 186.985 | 168.275 | 226.030 | 5.814 | 195.082 | 206.126 |
| postgres | idx_status_only | Q6: Aggregation by course_id for graded activities | 124.729 | 124.327 | 102.897 | 157.700 | 5.993 | 131.637 | 144.141 |
| postgres | idx_status_only | Q7: Broad score range where indexes are expected to help little | 117.118 | 116.119 | 96.669 | 149.693 | 8.039 | 126.206 | 131.368 |
| postgres | idx_student_id_only | Q1: Exact search by student_id | 30.993 | 29.565 | 13.292 | 41.357 | 4.827 | 33.375 | 34.341 |
| postgres | idx_student_id_only | Q2: Date range filtering by created_at | 108.912 | 108.552 | 89.132 | 151.177 | 6.631 | 116.475 | 127.182 |
| postgres | idx_student_id_only | Q3: Low-selectivity filtering by status | 109.174 | 109.214 | 89.837 | 144.444 | 6.281 | 119.043 | 129.973 |
| postgres | idx_student_id_only | Q4: Combined filtering by status and created_at | 109.496 | 109.501 | 87.931 | 157.322 | 7.731 | 121.738 | 134.997 |
| postgres | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 194.385 | 195.085 | 171.780 | 241.848 | 10.443 | 213.733 | 228.124 |
| postgres | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 141.952 | 143.937 | 120.747 | 212.977 | 10.446 | 162.422 | 179.617 |
| postgres | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 124.067 | 123.256 | 99.901 | 158.192 | 7.094 | 132.870 | 142.335 |
| postgres | no_indexes | Q1: Exact search by student_id | 93.165 | 91.962 | 68.482 | 117.125 | 6.442 | 98.743 | 106.619 |
| postgres | no_indexes | Q2: Date range filtering by created_at | 109.581 | 109.734 | 89.666 | 148.272 | 7.342 | 122.964 | 130.300 |
| postgres | no_indexes | Q3: Low-selectivity filtering by status | 109.614 | 110.309 | 92.394 | 146.454 | 7.187 | 122.605 | 134.624 |
| postgres | no_indexes | Q4: Combined filtering by status and created_at | 109.269 | 109.675 | 91.075 | 144.047 | 6.830 | 120.664 | 130.484 |
| postgres | no_indexes | Q5: Sort by created_at DESC with LIMIT | 190.768 | 192.979 | 170.402 | 265.317 | 10.035 | 209.714 | 224.215 |
| postgres | no_indexes | Q6: Aggregation by course_id for graded activities | 141.088 | 142.733 | 121.178 | 218.605 | 10.080 | 160.977 | 179.971 |
| postgres | no_indexes | Q7: Broad score range where indexes are expected to help little | 123.702 | 122.129 | 100.549 | 156.183 | 7.423 | 130.612 | 143.236 |

## Relative effect versus no_indexes

The ratio is calculated as median(no_indexes) / median(selected_config). Values above 1 indicate acceleration.

| DBMS | Index config | Query | Relative effect |
|---|---|---|---:|
| mongo | idx_student_id_only | Q1: Exact search by student_id | 459.93x |
| mongo | idx_student_id_only | Q2: Date range filtering by created_at | 1.04x |
| mongo | idx_student_id_only | Q3: Low-selectivity filtering by status | 1.03x |
| mongo | idx_student_id_only | Q4: Combined filtering by status and created_at | 1.01x |
| mongo | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 1.03x |
| mongo | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 1.05x |
| mongo | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 1.02x |
| mongo | idx_created_at_only | Q1: Exact search by student_id | 1.04x |
| mongo | idx_created_at_only | Q2: Date range filtering by created_at | 32.08x |
| mongo | idx_created_at_only | Q3: Low-selectivity filtering by status | 1.03x |
| mongo | idx_created_at_only | Q4: Combined filtering by status and created_at | 3.38x |
| mongo | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 673.68x |
| mongo | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 1.07x |
| mongo | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.02x |
| mongo | idx_status_only | Q1: Exact search by student_id | 1.04x |
| mongo | idx_status_only | Q2: Date range filtering by created_at | 1.04x |
| mongo | idx_status_only | Q3: Low-selectivity filtering by status | 6.20x |
| mongo | idx_status_only | Q4: Combined filtering by status and created_at | 1.30x |
| mongo | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 1.04x |
| mongo | idx_status_only | Q6: Aggregation by course_id for graded activities | 1.35x |
| mongo | idx_status_only | Q7: Broad score range where indexes are expected to help little | 1.03x |
| mongo | idx_status_created_at_only | Q1: Exact search by student_id | 1.04x |
| mongo | idx_status_created_at_only | Q2: Date range filtering by created_at | 1.04x |
| mongo | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 6.04x |
| mongo | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 128.56x |
| mongo | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 1.05x |
| mongo | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 0.73x |
| mongo | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.03x |
| mongo | idx_course_score_only | Q1: Exact search by student_id | 1.01x |
| mongo | idx_course_score_only | Q2: Date range filtering by created_at | 1.02x |
| mongo | idx_course_score_only | Q3: Low-selectivity filtering by status | 1.01x |
| mongo | idx_course_score_only | Q4: Combined filtering by status and created_at | 1.00x |
| mongo | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 1.04x |
| mongo | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 1.09x |
| mongo | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 1.02x |
| mongo | all_indexes | Q1: Exact search by student_id | 477.69x |
| mongo | all_indexes | Q2: Date range filtering by created_at | 33.74x |
| mongo | all_indexes | Q3: Low-selectivity filtering by status | 6.26x |
| mongo | all_indexes | Q4: Combined filtering by status and created_at | 127.05x |
| mongo | all_indexes | Q5: Sort by created_at DESC with LIMIT | 667.29x |
| mongo | all_indexes | Q6: Aggregation by course_id for graded activities | 1.36x |
| mongo | all_indexes | Q7: Broad score range where indexes are expected to help little | 1.02x |
| mysql | idx_student_id_only | Q1: Exact search by student_id | 8.09x |
| mysql | idx_student_id_only | Q2: Date range filtering by created_at | 1.00x |
| mysql | idx_student_id_only | Q3: Low-selectivity filtering by status | 1.00x |
| mysql | idx_student_id_only | Q4: Combined filtering by status and created_at | 1.00x |
| mysql | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 1.02x |
| mysql | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 1.04x |
| mysql | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 1.00x |
| mysql | idx_created_at_only | Q1: Exact search by student_id | 1.00x |
| mysql | idx_created_at_only | Q2: Date range filtering by created_at | 5.02x |
| mysql | idx_created_at_only | Q3: Low-selectivity filtering by status | 1.00x |
| mysql | idx_created_at_only | Q4: Combined filtering by status and created_at | 1.62x |
| mysql | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 15.97x |
| mysql | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 1.02x |
| mysql | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.00x |
| mysql | idx_status_only | Q1: Exact search by student_id | 1.00x |
| mysql | idx_status_only | Q2: Date range filtering by created_at | 0.99x |
| mysql | idx_status_only | Q3: Low-selectivity filtering by status | 2.53x |
| mysql | idx_status_only | Q4: Combined filtering by status and created_at | 0.74x |
| mysql | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 0.99x |
| mysql | idx_status_only | Q6: Aggregation by course_id for graded activities | 0.86x |
| mysql | idx_status_only | Q7: Broad score range where indexes are expected to help little | 1.00x |
| mysql | idx_status_created_at_only | Q1: Exact search by student_id | 1.00x |
| mysql | idx_status_created_at_only | Q2: Date range filtering by created_at | 5.01x |
| mysql | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 2.51x |
| mysql | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 6.07x |
| mysql | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 1.00x |
| mysql | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 0.41x |
| mysql | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.00x |
| mysql | idx_course_score_only | Q1: Exact search by student_id | 0.99x |
| mysql | idx_course_score_only | Q2: Date range filtering by created_at | 1.00x |
| mysql | idx_course_score_only | Q3: Low-selectivity filtering by status | 0.99x |
| mysql | idx_course_score_only | Q4: Combined filtering by status and created_at | 0.99x |
| mysql | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 1.00x |
| mysql | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 0.12x |
| mysql | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 0.90x |
| mysql | all_indexes | Q1: Exact search by student_id | 8.07x |
| mysql | all_indexes | Q2: Date range filtering by created_at | 4.99x |
| mysql | all_indexes | Q3: Low-selectivity filtering by status | 2.51x |
| mysql | all_indexes | Q4: Combined filtering by status and created_at | 6.02x |
| mysql | all_indexes | Q5: Sort by created_at DESC with LIMIT | 15.29x |
| mysql | all_indexes | Q6: Aggregation by course_id for graded activities | 0.88x |
| mysql | all_indexes | Q7: Broad score range where indexes are expected to help little | 0.89x |
| postgres | idx_student_id_only | Q1: Exact search by student_id | 3.01x |
| postgres | idx_student_id_only | Q2: Date range filtering by created_at | 1.01x |
| postgres | idx_student_id_only | Q3: Low-selectivity filtering by status | 1.00x |
| postgres | idx_student_id_only | Q4: Combined filtering by status and created_at | 1.00x |
| postgres | idx_student_id_only | Q5: Sort by created_at DESC with LIMIT | 0.98x |
| postgres | idx_student_id_only | Q6: Aggregation by course_id for graded activities | 0.99x |
| postgres | idx_student_id_only | Q7: Broad score range where indexes are expected to help little | 1.00x |
| postgres | idx_created_at_only | Q1: Exact search by student_id | 1.01x |
| postgres | idx_created_at_only | Q2: Date range filtering by created_at | 3.56x |
| postgres | idx_created_at_only | Q3: Low-selectivity filtering by status | 1.01x |
| postgres | idx_created_at_only | Q4: Combined filtering by status and created_at | 1.80x |
| postgres | idx_created_at_only | Q5: Sort by created_at DESC with LIMIT | 6.18x |
| postgres | idx_created_at_only | Q6: Aggregation by course_id for graded activities | 1.01x |
| postgres | idx_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.12x |
| postgres | idx_status_only | Q1: Exact search by student_id | 1.14x |
| postgres | idx_status_only | Q2: Date range filtering by created_at | 1.01x |
| postgres | idx_status_only | Q3: Low-selectivity filtering by status | 2.36x |
| postgres | idx_status_only | Q4: Combined filtering by status and created_at | 1.17x |
| postgres | idx_status_only | Q5: Sort by created_at DESC with LIMIT | 1.02x |
| postgres | idx_status_only | Q6: Aggregation by course_id for graded activities | 1.13x |
| postgres | idx_status_only | Q7: Broad score range where indexes are expected to help little | 1.06x |
| postgres | idx_status_created_at_only | Q1: Exact search by student_id | 1.15x |
| postgres | idx_status_created_at_only | Q2: Date range filtering by created_at | 1.76x |
| postgres | idx_status_created_at_only | Q3: Low-selectivity filtering by status | 2.36x |
| postgres | idx_status_created_at_only | Q4: Combined filtering by status and created_at | 3.53x |
| postgres | idx_status_created_at_only | Q5: Sort by created_at DESC with LIMIT | 1.02x |
| postgres | idx_status_created_at_only | Q6: Aggregation by course_id for graded activities | 1.13x |
| postgres | idx_status_created_at_only | Q7: Broad score range where indexes are expected to help little | 1.12x |
| postgres | idx_course_score_only | Q1: Exact search by student_id | 1.15x |
| postgres | idx_course_score_only | Q2: Date range filtering by created_at | 1.01x |
| postgres | idx_course_score_only | Q3: Low-selectivity filtering by status | 1.01x |
| postgres | idx_course_score_only | Q4: Combined filtering by status and created_at | 1.00x |
| postgres | idx_course_score_only | Q5: Sort by created_at DESC with LIMIT | 1.02x |
| postgres | idx_course_score_only | Q6: Aggregation by course_id for graded activities | 1.01x |
| postgres | idx_course_score_only | Q7: Broad score range where indexes are expected to help little | 1.58x |
| postgres | all_indexes | Q1: Exact search by student_id | 3.01x |
| postgres | all_indexes | Q2: Date range filtering by created_at | 3.54x |
| postgres | all_indexes | Q3: Low-selectivity filtering by status | 2.35x |
| postgres | all_indexes | Q4: Combined filtering by status and created_at | 3.55x |
| postgres | all_indexes | Q5: Sort by created_at DESC with LIMIT | 6.20x |
| postgres | all_indexes | Q6: Aggregation by course_id for graded activities | 1.13x |
| postgres | all_indexes | Q7: Broad score range where indexes are expected to help little | 1.59x |
