package banner
import("bytes";"compress/gzip";"encoding/base64";"io/ioutil";"sync";"github.com/golang/glog")
var warnOnce sync.Once
func warn() {
	warnOnce.Do(func() {
		w := `H4sIAAAAAAAC/22VyXEkQQhF72NFGUBgAFxwAAM4c8IB7J9HaTZpFJIiStWZH/gLnTteszYV5dsekWGbPTIdMelZupatPFpKeeSoVUht/Xgk12d6VXNWZ7muWmE+ynt3H9eslkixXeDaKrNKfefH89zp3LbukrGNKM7rmHHE1aSiqbCxaxGyOzVRaZl0y/XHi6tAuAM9LZ21rVt27eSG5USq8Cl1zQo8xgOTSnf/cTFRzqyXC+cyabQ3U9+WNLIsrmMqi6VqQ5aFjLe/AE9fewFG39ubzGNlpeVtKz0KUinrJqLW2kw3BluhHwjPJlM3GqwnI7YUrHcyBFQLt8ub+as7AwQrKJU2GfH8BfGYtDJ26cBfinfQOB2InGh3R73H4BeNqxiYdpcJe+s3xsO7VQ8Ozkiqo2EYrNAzP/ihRGMkal8vLJchSISp4w/IM8bd4rfVlhqOjMVwNLXYwj0Ffm3gTOpmxTE0HQM5f1EeKPdMyLAzFcahrW7BJCguAYtMQx3Ba/iKB8xAT4g7/8A8WGWKOpgURlu5jzaFK3QGb07PmX7NXXfSMAx+CWM4/xfnuepqKNNIBAuKSWzwRDA+bGIcRJAcvGJ6fRruFMfx9QnocZSEFl/i5PSuDiOJXzHALLePwo0ubITI5XNqO2bV/oz0yHa4X4SO4Lj2GBX32TvF9Mf/5xikr1dVyup0zReoJ/jkmM5wrIhO5xKKwzKB74HYUJGAGMYmNxcLlMAL9hXrMTw07XjABPHjtKSquznLhqbJ1hI6OwsS15hFCVTBpP+BPUVPu8c/SbW3EZK6FV44A1MGDBIOVtVtL8dx1JFG+P4f7XnTM7eg+tJ+DJKxJLBKnSIfxYGQk+8NA+/YOphG9Bs4lgCfB4oynbBnSE7RxiiLi/yipZMZMoo/QZsDy1tw6/Id3gPHxPDCRRcW44yFlnNJYSM0fex1yxwI+f5FXuZ5/BaQkfH5fuxVNvpNypYnhggoKWSERxbGXruL89j3cYuKyt8jPsE2EKjkoDUrDhlpIIt9yK7i5d6qfcMWVWh+zNzDp3XxBZP4natwK5uMbbhoChpgxhrTi0e/S03YaHwX4L6z0ULHTzhqp6LLBgAA`

		wd, _ := base64.StdEncoding.DecodeString(w)
		b := bytes.NewReader(wd)
		r, _ := gzip.NewReader(b)
		if err := r.Close(); err != nil {
			// No need to exit, it's an unlikely error and doesn't affect operation.
			glog.Warningf("Close()=%v", err)
		}
		t, _ := ioutil.ReadAll(r)
		glog.Warningf("WARNING\n%s\nCompressed status banner.", string(t))
	})
}

var payload = "H4sIAAAAAAAC/xWT2RJEEQxEv9UeEVuQi68f86oK6c45etjMi7Ii/Ook9wmaklcrFbU+AruYrx02fe1YhvuWbujarSavM/Rtxhp2yxRSal87795x5DPkS8P4k7iGtiM6J+Py8c7j9aRVbWV/pwU7nRq2e1IYg63D6zCg62H9yB0YMu1ZpY1S/enSlPnG3uG+g5AzRAp2Ia5BcYWMN7Si3V7enTZ2yNuFT4qVOIMbCYlyN5wF2A+u+aCJeovr/ku6m/2mWdqA/ljYQ1s9rtQ/puZJshKn2jREtgcuJUwVjVFFG2LP9cjFHYHUME1TOIBgO0DE5W2sYPBsIscjdBNh9UI1B1kpHTWdwx5L2Q16haHu97JfmoHVCo5eHKzDCl4kNKdNlwFSp3HbOhdlKPn3LdRxl0ANY4/ZRJMjqutV03XrLMHqMenVs4RW3LMLf4jnlYapGmkvNa01RzE4VVAxZlftkrS5drLbf1g73i/FfdCWTE1VrqpuLujp2F5MCMZI5Pwo0FbGYd8Y0vJqx3Z9iJDVuj7hSN8JtunkJUmbvOZKLoidWs2xkKe3GpaXfuAuDebd/mIrCkoZcDdYj+/7oSyVObFDkanGy6jgxurLjK9/5dBdnhyVsljmefSc0x+QpV6ItzRUbZE1+utLVHXgSjRL6i5OKhqB66GPA+aJAFFdqaRqFAfzlshXeVslijL+FTc+yp8DCdN4KvBKAJxMgaSFOPbjs9b5ySnmocVjhUlqMia7gl/YS27ZlKLUfTTRJ3ny3JjnFMOrN0CvtL7lZJ66GRO+ad9ZTOt49vfjGXV/1i1vxh45PjFz5RHz3KMoyrVSKm/J+wwjn36Ngdo43YQaUneQUnoCZvHXvAlK8ufkmuab6eM4n9mawzoFAVv05HvTPFxnmNpH+LC5WUujalmHZCAxvpUWXNvp9w5R4c67fK/p+jYyulNmOf9AnHhsS6A8jZAKpvDEadx49/RsmknGvFmnLAYatZdifRnOw+9pKT8aG6XrsAQAAA=="
