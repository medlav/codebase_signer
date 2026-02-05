# ---
# project: Codebase Signer
# file: main.py
# author: medlav
# created: 2026-02-05
# license: BSD-3-CLAUSE
# ---
# Copyright (c) 2026 medlav
#
# This is free software, this software was made as a custom private solution.
# The code and derived executables and binaries are meant to be used only privately.
# The following code is not meant to be shared as open source or free software.
# If this code is shared publicly for research, audit or teaching purposes
# it should be considered as Unlicensed code.
#
# THE AUTHOR IS NOT LIABLE FOR ANY MISUSE OF THE CODE.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import test1
import test2


def main():
    test1.compound(0.02, 10, True)
    test2.main()


if __name__ == "__main__":
    main()
