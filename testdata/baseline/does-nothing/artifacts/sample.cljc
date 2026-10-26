(ns sample.shared)

(defn log-message []
  #?(:clj  (clojure.tools.logging/info "this sample does nothing")
     :cljs (js/console.info "this sample does nothing")))
