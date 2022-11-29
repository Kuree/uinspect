#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

namespace py = pybind11;

static Py_ssize_t code_extra_index = 0;

class Frame {
public:
    explicit Frame(PyFrameObject *frame) : frame_(frame) { }

    Frame() : Frame(1) {}

    explicit Frame(uint32_t num_frames_back) {
        frame_ = PyThreadState_Get()->frame;
        uint32_t i = 0;
        while (frame_ && (++i) < num_frames_back) {
            frame_ = frame_->f_back;
        }

        update();
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

    py::dict update() {
        if (!frame_) return {};
        lineno = PyFrame_GetLineNumber(frame_);
        /*
        py::dict res;
        if (stack_head_) {
            while (stack_head_ != frame_->f_valuestack) {
                printf("%p\n", stack_head_);
                stack_head_++;
            }
        }

        stack_head_ = frame_->f_valuestack;
        return res;
         */
    }

    uint32_t lineno = 0;

private:
    PyFrameObject *frame_;
};

Frame *get_frame(uint32_t num_frames_back) {
    auto frame = PyThreadState_Get()->frame;
    uint32_t i = 0;
    while (frame && (++i) < num_frames_back) {
        frame = frame->f_back;
    }

    if (!frame) {
        return nullptr;
    }

    // get frame object
    Frame *frame_res;
    auto *frame_ptr = reinterpret_cast<void *>(frame_res);
    auto res = _PyCode_GetExtra(&frame->f_code->ob_base, code_extra_index, &frame_ptr);
    if (res != 0) {
        frame_res = new Frame(frame);
        _PyCode_SetExtra(&frame->f_code->ob_base, code_extra_index, frame_res);
    }
    return frame_res;
}

void init_frame(py::module &m) {
    auto frame = py::class_<Frame>(m, "Frame")
                     .def(py::init(&get_frame), py::arg("num_frames_back") = 1,
                          py::return_value_policy::reference_internal);
    frame.def_property_readonly("filename", &Frame::get_filename);
    frame.def_readonly("lineno", &Frame::lineno);
    frame.def_property_readonly("locals", &Frame::get_locals);
    frame.def("update", &Frame::update);
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

void free_storage(void *ptr) {
    auto *frame = reinterpret_cast<Frame *>(ptr);
    delete frame;
}

void init_code_extra_index() { code_extra_index = _PyEval_RequestCodeExtraIndex(&free_storage); }

PYBIND11_MODULE(uinspect, m) {
    init_code_extra_index();
    init_frame(m);
    init_func(m);
}