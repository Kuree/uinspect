#include <filesystem>

#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

namespace py = pybind11;

PyFrameObject *get_frame() {
#if PY_MINOR_VERSION >= 10
    return PyEval_GetFrame();
#else
    return PyThreadState_Get()->frame;
#endif
}

class Frame {
public:
    explicit Frame(PyFrameObject *frame) : frame_(frame) { setup_lineno(); }

    Frame() : Frame(1) {}

    explicit Frame(uint32_t num_frames_back) {
        frame_ = get_frame();
        uint32_t i = 0;
        while (frame_ && (++i) < num_frames_back) {
            frame_ = frame_->f_back;
        }
        setup_lineno();
    }

    [[nodiscard]] py::handle get_filename() const {
        if (!frame_) return py::none();
        struct py::detail::string_caster<std::string> filename;
        py::handle handle(frame_->f_code->co_filename);
        return handle;
    }

    [[nodiscard]] py::handle get_locals() const {
        if (!frame_) return py::none();
        PyFrame_FastToLocals(frame_);
        return frame_->f_locals;
    }

    void collect_vars() {
        if (!frame_) return;
        known_vars_.clear();
        PyFrame_FastToLocals(frame_);
        auto dict = py::cast<py::dict>(py::handle(frame_->f_locals));
        known_vars_.reserve(dict.size());
        for (auto handle : dict) {
            known_vars_.emplace_back(py::cast<std::string>(handle.first));
        }
    }

    std::vector<std::string> diff(Frame &frame) const {
        if (frame.known_vars_.size() == known_vars_.size()) {
            return {};
        }
        bool other_longer = frame.known_vars_.size() > known_vars_.size();
        auto const &long_list = other_longer ? frame.known_vars_ : known_vars_;
        auto const &short_list = other_longer ? known_vars_ : frame.known_vars_;
        std::vector<std::string> res;
        res.reserve(long_list.size() - short_list.size());
        for (auto i = short_list.size(); i < long_list.size(); i++) {
            auto name = long_list[i];
            res.emplace_back(name);
        }
        return res;
    }

    [[nodiscard]] py::dict get_globals() const {
        if (!frame_) return {};
        return py::cast<py::dict>(frame_->f_globals);
    }

    int lineno = 0;

private:
    PyFrameObject *frame_;
    std::vector<std::string> known_vars_;

    void setup_lineno() { lineno = frame_ ? PyFrame_GetLineNumber(frame_) : 0; }
};

class FrameWalker {
public:
    explicit FrameWalker(std::unordered_set<std::string> filenames)
        : filenames_(std::move(filenames)) {}

    std::pair<std::string, uint32_t> get_location() const {
        auto *frame = get_frame();

        while (frame) {
            auto filename = py::cast<std::string>(frame->f_code->co_filename);
            auto basename = std::filesystem::path(filename).filename().string();
            if (filenames_.find(basename) == filenames_.end()) {
                uint32_t line = PyFrame_GetLineNumber(frame);
                return {filename, line};
            }
            frame = frame->f_back;
        }

        return {};
    }

private:
    std::unordered_set<std::string> filenames_;
};

void init_frame(py::module &m) {
    auto frame = py::class_<Frame>(m, "Frame")
                     .def(py::init<>())
                     .def(py::init<uint32_t>(), py::arg("num_frames_back"));
    frame.def_property_readonly("filename", &Frame::get_filename);
    frame.def_readonly("lineno", &Frame::lineno);
    frame.def_property_readonly("locals", &Frame::get_locals);
    frame.def("diff", &Frame::diff);
    frame.def("collect_vars", &Frame::collect_vars);
    frame.def_property_readonly("globals", &Frame::get_globals);
}

void init_frame_walker(py::module &m) {
    auto walker = py::class_<FrameWalker>(m, "FrameWalker");
    walker.def(py::init<std::unordered_set<std::string>>());
    walker.def("get_location", &FrameWalker::get_location);
}

void init_func(py::module &m) {
    m.def(
        "get_location",
        [](uint32_t num_frames_back) {
            // this avoids creating an object in Python
            Frame f(num_frames_back);
            return std::make_pair(f.get_filename(), f.lineno);
        },
        py::arg("num_frames_back") = 1);
}

PYBIND11_MODULE(uinspect, m) {
    init_frame(m);
    init_frame_walker(m);
    init_func(m);
}