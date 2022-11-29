#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

namespace py = pybind11;

class Frame {
public:
    explicit Frame(PyFrameObject *frame) : frame_(frame) {}

    Frame() : Frame(1) {}

    explicit Frame(uint32_t num_frames_back) {
        frame_ = PyThreadState_Get()->frame;
        uint32_t i = 0;
        while (frame_ && (++i) < num_frames_back) {
            frame_ = frame_->f_back;
        }
    }

    [[nodiscard]] py::handle get_filename() const {
        if (!frame_) return py::none();
        struct py::detail::string_caster<std::string> filename;
        py::handle handle(frame_->f_code->co_filename);
        return handle;
    }

    [[nodiscard]] uint32_t get_lineno() const {
        if (!frame_) return 0;
        return PyFrame_GetLineNumber(frame_);
    }

    [[nodiscard]] py::handle get_locals() const {
        if (!frame_) return py::none();
        PyFrame_FastToLocals(frame_);
        return frame_->f_locals;
    }

    py::dict diff(Frame &frame) const { return {}; }

private:
    PyFrameObject *frame_;
};

void init_frame(py::module &m) {
    auto frame = py::class_<Frame>(m, "Frame")
                     .def(py::init<>())
                     .def(py::init<uint32_t>(), py::arg("num_frames_back"));
    frame.def_property_readonly("filename", &Frame::get_filename);
    frame.def_property_readonly("lineno", &Frame::get_lineno);
    frame.def_property_readonly("locals", &Frame::get_locals);
    frame.def("diff", &Frame::diff);
}

void init_func(py::module &m) {
    m.def(
        "get_location",
        [](uint32_t num_frames_back) {
            // this avoids creating an object in Python
            Frame f(num_frames_back);
            return std::make_pair(f.get_filename(), f.get_lineno());
        },
        py::arg("num_frames_back") = 1);
}

PYBIND11_MODULE(uinspect, m) {
    init_frame(m);
    init_func(m);
}